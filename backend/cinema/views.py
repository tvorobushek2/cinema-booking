from rest_framework import generics
from rest_framework.response import Response
from django.core.cache import cache
from .models import Session, Seat
from .serializers import SessionSerializer


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
        from rest_framework import status
        
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
        
        # ВРЕМЕННО: все места свободны
        booked_seat_ids = []
        
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