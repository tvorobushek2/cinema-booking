 
from rest_framework import serializers
from .models import Booking

class BookingCreateSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()
    seat_ids = serializers.ListField(child=serializers.IntegerField(), min_length=1)

class BookingResponseSerializer(serializers.ModelSerializer):
    session_id = serializers.IntegerField(source='session.id')
    seat_id = serializers.IntegerField(source='seat.id')
    
    class Meta:
        model = Booking
        fields = ['id', 'session_id', 'seat_id', 'status', 'expires_at', 'created_at']