from rest_framework import generics, status
from rest_framework.response import Response
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import Session, Seat, Booking
from .serializers import (
    SessionSerializer, 
    SeatWithStatusSerializer,
    BookingCreateSerializer,
    BookingResponseSerializer
)


class SessionListView(generics.ListAPIView):
    serializer_class = SessionSerializer
    
    def get_queryset(self):
        return Session.objects.select_related('hall').all()
    
    def list(self, request, *args, **kwargs):
        cache_key = 'sessions_list'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        cache.set(cache_key, data, 600)
        
        return Response(data)


class SessionSeatsView(generics.RetrieveAPIView):
    def get(self, request, pk):
        try:
            session = Session.objects.select_related('hall').get(pk=pk)
        except Session.DoesNotExist:
            return Response(
                {'error': 'Session not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        seats = Seat.objects.filter(
            row__hall=session.hall
        ).select_related('row', 'row__hall')
        
        booked_seat_ids = Booking.objects.filter(
            session=session,
            status__in=['awaiting', 'paid']
        ).values_list('seat_id', flat=True)
        
        result = []
        for seat in seats:
            seat_data = {
                'seat_id': seat.id,
                'row': seat.row.number,
                'number': seat.number,
                'type': seat.type,
                'price': seat.price,
                'status': 'taken' if seat.id in booked_seat_ids else 'free'
            }
            result.append(seat_data)
        
        return Response(result)


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingCreateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_id = serializer.validated_data['user_id']
        session_id = serializer.validated_data['session_id']
        seat_ids = serializer.validated_data['seat_ids']
        
        try:
            with transaction.atomic():
                session = Session.objects.select_for_update().get(pk=session_id)
                
                seats = Seat.objects.filter(
                    id__in=seat_ids,
                    row__hall=session.hall
                ).select_for_update()
                
                if len(seats) != len(seat_ids):
                    return Response(
                        {'error': 'Some seats not found or belong to different hall'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                occupied_seats = Booking.objects.filter(
                    session=session,
                    seat_id__in=seat_ids,
                    status__in=['awaiting', 'paid']
                ).values_list('seat_id', flat=True)
                
                if occupied_seats:
                    return Response(
                        {
                            'error': 'Some seats are already booked',
                            'occupied_seats': list(occupied_seats)
                        },
                        status=status.HTTP_409_CONFLICT
                    )
                
                now = timezone.now()
                expires_at = now + timedelta(minutes=15)
                
                bookings = []
                total_price = 0
                
                for seat in seats:
                    booking = Booking.objects.create(
                        user_id=user_id,
                        session=session,
                        seat=seat,
                        status='awaiting',
                        expires_at=expires_at
                    )
                    bookings.append(booking)
                    total_price += float(seat.price)
                
                cache.delete('sessions_list')
                
                return Response(
                    {
                        'booking_ids': [b.id for b in bookings],
                        'expires_at': expires_at.isoformat(),
                        'total_price': total_price,
                        'status': 'awaiting'
                    },
                    status=status.HTTP_201_CREATED
                )
        except Session.DoesNotExist:
            return Response(
                {'error': 'Session not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class BookingPayView(generics.GenericAPIView):
    def post(self, request, pk):
        try:
            with transaction.atomic():
                booking = Booking.objects.select_for_update().get(pk=pk)
                
                if booking.status != 'awaiting':
                    return Response(
                        {'error': f'Booking is {booking.status}, cannot pay'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                if booking.is_expired():
                    booking.status = 'expired'
                    booking.save(update_fields=['status'])
                    return Response(
                        {'error': 'Booking has expired'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                booking.status = 'paid'
                booking.save(update_fields=['status'])
                
                cache.delete('sessions_list')
                
                return Response({
                    'status': 'paid',
                    'booking_id': booking.id
                })
                
        except Booking.DoesNotExist:
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class BookingExtendView(generics.GenericAPIView):
    def post(self, request, pk):
        try:
            with transaction.atomic():
                booking = Booking.objects.select_for_update().get(pk=pk)
                
                if booking.status != 'awaiting':
                    return Response(
                        {'error': f'Booking is {booking.status}, cannot extend'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                if booking.is_expired():
                    booking.status = 'expired'
                    booking.save(update_fields=['status'])
                    return Response(
                        {'error': 'Booking has expired'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                booking.expires_at += timedelta(minutes=5)
                booking.save(update_fields=['expires_at'])
                
                return Response({
                    'new_expires_at': booking.expires_at.isoformat()
                })
                
        except Booking.DoesNotExist:
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )