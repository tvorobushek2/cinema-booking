 
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingCreateSerializer, BookingResponseSerializer
import logging
import sys
import os

# Добавляем путь к моделям Ильи
sys.path.append(os.path.join(os.path.dirname(__file__), '../../frontend'))

logger = logging.getLogger(__name__)

@api_view(['POST'])
def create_booking(request):
    serializer = BookingCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    session_id = serializer.validated_data['session_id']
    seat_ids = serializer.validated_data['seat_ids']

    try:
        with transaction.atomic():
            from cinema.models import Session, Seat
            
            try:
                session = Session.objects.get(id=session_id)
            except Session.DoesNotExist:
                return Response(
                    {"error": f"Сеанс с id {session_id} не найден"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            seats = Seat.objects.filter(id__in=seat_ids, hall=session.hall)
            if seats.count() != len(seat_ids):
                return Response(
                    {"error": "Некоторые места не принадлежат залу этого сеанса"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            existing_bookings = Booking.objects.filter(
                session_id=session_id,
                seat_id__in=seat_ids
            ).exclude(status='expired').select_for_update()

            if existing_bookings.exists():
                occupied_seats = list(existing_bookings.values_list('seat_id', flat=True))
                return Response(
                    {"error": "Некоторые места уже забронированы", "occupied_seats": occupied_seats},
                    status=status.HTTP_409_CONFLICT
                )

            now = timezone.now()
            expires_at = now + timezone.timedelta(minutes=15)
            bookings_to_create = []
            for seat_id in seat_ids:
                bookings_to_create.append(
                    Booking(
                        session_id=session_id,
                        seat_id=seat_id,
                        expires_at=expires_at,
                        status='awaiting'
                    )
                )
            Booking.objects.bulk_create(bookings_to_create)

            new_bookings = Booking.objects.filter(
                session_id=session_id,
                seat_id__in=seat_ids,
                status='awaiting'
            )
            response_serializer = BookingResponseSerializer(new_bookings, many=True)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Error in create_booking: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def pay_booking(request, booking_id):
    try:
        with transaction.atomic():
            booking = Booking.objects.select_for_update().get(id=booking_id)

            if booking.status == 'paid':
                return Response(
                    {"error": "Бронирование уже оплачено"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if booking.status == 'expired':
                return Response(
                    {"error": "Бронирование просрочено"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if booking.expires_at < timezone.now():
                booking.status = 'expired'
                booking.save()
                return Response(
                    {"error": "Бронирование просрочено"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            import time
            time.sleep(2)

            booking.status = 'paid'
            booking.save()

            return Response(
                {"status": "paid", "booking_id": booking.id},
                status=status.HTTP_200_OK
            )

    except Booking.DoesNotExist:
        return Response(
            {"error": "Бронирование не найдено"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
def extend_booking(request, booking_id):
    try:
        with transaction.atomic():
            booking = Booking.objects.select_for_update().get(id=booking_id)

            if booking.status != 'awaiting':
                return Response(
                    {"error": "Продлить можно только ожидающее бронирование"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            booking.expires_at = timezone.now() + timezone.timedelta(minutes=5)
            booking.save()

            return Response(
                {"new_expires_at": booking.expires_at},
                status=status.HTTP_200_OK
            )

    except Booking.DoesNotExist:
        return Response(
            {"error": "Бронирование не найдено"},
            status=status.HTTP_404_NOT_FOUND
        )