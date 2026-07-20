from rest_framework import serializers
from .models import Hall, Row, Seat, Session


class SessionSerializer(serializers.ModelSerializer):
    """Сериализатор для списка сеансов"""
    hall_name = serializers.CharField(source='hall.name', read_only=True)
    
    class Meta:
        model = Session
        fields = ['id', 'title', 'started_at', 'duration', 'hall_id', 'hall_name']

class SessionSerializer(serializers.ModelSerializer):
    """Сериализатор для списка сеансов"""
    hall_name = serializers.CharField(source='hall.name', read_only=True)
    
    class Meta:
        model = Session
        fields = ['id', 'title', 'poster', 'started_at', 'duration', 'hall_id', 'hall_name']


class SeatSerializer(serializers.ModelSerializer):
    """Сериализатор для места с информацией о ряде и зале"""
    row = serializers.IntegerField(source='row.number', read_only=True)
    hall = serializers.IntegerField(source='row.hall.number', read_only=True)
    
    class Meta:
        model = Seat
        fields = ['id', 'row', 'number', 'type', 'price', 'hall']


class SeatWithStatusSerializer(serializers.Serializer):
    """Сериализатор для места со статусом (free/taken)"""
    seat_id = serializers.IntegerField()
    row = serializers.IntegerField()
    number = serializers.IntegerField()
    type = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    status = serializers.CharField()  # 'free' или 'taken'

from .models import Booking


class BookingCreateSerializer(serializers.Serializer):
    """Сериализатор для создания брони"""
    user_id = serializers.IntegerField()
    session_id = serializers.IntegerField()
    seat_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        help_text="Список ID мест для бронирования"
    )


class BookingResponseSerializer(serializers.ModelSerializer):
    """Сериализатор ответа о созданной брони"""
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = ['id', 'user_id', 'session_id', 'seat_id', 'status', 
                  'created_at', 'expires_at', 'total_price']
    
    def get_total_price(self, obj):
        return obj.seat.price