from rest_framework import serializers
from .models import Hall, Row, Seat, Session


class SessionSerializer(serializers.ModelSerializer):
    """Сериализатор для списка сеансов"""
    hall_name = serializers.CharField(source='hall.name', read_only=True)
    
    class Meta:
        model = Session
        fields = ['id', 'title', 'started_at', 'duration', 'hall_id', 'hall_name']


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