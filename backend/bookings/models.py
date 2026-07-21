from django.db import models
from django.utils import timezone

class Booking(models.Model):
    session = models.ForeignKey(
        'cinema.Session',
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    seat = models.ForeignKey(
        'cinema.Seat',
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    user_id = models.IntegerField(default=1)

    STATUS_CHOICES = [
        ('awaiting', 'Ожидает оплаты'),
        ('paid', 'Оплачено'),
        ('expired', 'Просрочено'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='awaiting')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        unique_together = ('session', 'seat')
        indexes = [
            models.Index(fields=['session', 'seat']),
            models.Index(fields=['status', 'expires_at']),
        ]

    def __str__(self):
        return f"Booking {self.id} — {self.seat} (Session {self.session.id})" 
