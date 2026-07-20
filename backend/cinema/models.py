from django.db import models
from django.core.validators import MinValueValidator


class Hall(models.Model):
    """Кинотеатральный зал"""
    number = models.IntegerField(
        unique=True,
        validators=[MinValueValidator(1)],
        help_text="Номер зала"
    )
    name = models.CharField(
        max_length=50,
        help_text="Название зала"
    )

    class Meta:
        ordering = ['number']
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'

    def __str__(self):
        return f"Зал {self.number} ({self.name})"


class Row(models.Model):
    """Ряд в зале"""
    hall = models.ForeignKey(
        Hall,
        on_delete=models.CASCADE,
        related_name='rows',
        help_text="Зал"
    )
    number = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Номер ряда"
    )

    class Meta:
        ordering = ['hall', 'number']
        unique_together = ['hall', 'number']
        verbose_name = 'Ряд'
        verbose_name_plural = 'Ряды'

    def __str__(self):
        return f"Зал {self.hall.number}, Ряд {self.number}"


class Seat(models.Model):
    """Место в ряду"""
    SEAT_TYPES = [
        ('standard', 'Стандартное'),
        ('vip', 'VIP'),
    ]

    row = models.ForeignKey(
        Row,
        on_delete=models.CASCADE,
        related_name='seats',
        help_text="Ряд"
    )
    number = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Номер места"
    )
    type = models.CharField(
        max_length=10,
        choices=SEAT_TYPES,
        default='standard',
        help_text="Тип места"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Цена билета"
    )

    class Meta:
        ordering = ['row', 'number']
        unique_together = ['row', 'number']
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return f"Зал {self.row.hall.number}, Ряд {self.row.number}, Место {self.number}"


class Session(models.Model):
    """Сеанс фильма"""
    hall = models.ForeignKey(
        Hall,
        on_delete=models.RESTRICT,
        related_name='sessions',
        help_text="Зал"
    )
    title = models.CharField(
        max_length=200,
        help_text="Название фильма"
    )
class Session(models.Model):
    """Сеанс фильма"""
    hall = models.ForeignKey(
        Hall,
        on_delete=models.RESTRICT,
        related_name='sessions',
        help_text="Зал"
    )
    title = models.CharField(
        max_length=200,
        help_text="Название фильма"
    )
    poster = models.URLField(
        blank=True,
        null=True,
        help_text="URL постера фильма"
    )
    started_at = models.DateTimeField(
        help_text="Время начала сеанса"
    )
    duration = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Длительность в минутах"
    )
    started_at = models.DateTimeField(
        help_text="Время начала сеанса"
    )
    duration = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Длительность в минутах"
    )

    class Meta:
        ordering = ['started_at']
        verbose_name = 'Сеанс'
        verbose_name_plural = 'Сеансы'

    def __str__(self):
        return f"{self.title} ({self.started_at.strftime('%d.%m.%Y %H:%M')})"

from django.utils import timezone
from datetime import timedelta


class Booking(models.Model):
    """Бронь места на сеанс"""
    STATUS_CHOICES = [
        ('awaiting', 'Ожидает оплаты'),
        ('paid', 'Оплачена'),
        ('expired', 'Истекла'),
    ]

    user_id = models.IntegerField(
        help_text="ID пользователя (заглушка)"
    )
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text="Сеанс"
    )
    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text="Место"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='awaiting',
        help_text="Статус брони"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Время создания"
    )
    expires_at = models.DateTimeField(
        help_text="Время истечения брони"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
        # Защита от дублей на уровне Django
        constraints = [
            models.UniqueConstraint(
                fields=['session', 'seat'],
                condition=models.Q(status__in=['awaiting', 'paid']),
                name='unique_active_booking'
            )
        ]

    def __str__(self):
        return f"Бронь #{self.id} - {self.session.title} - Место {self.seat}"

    def is_expired(self):
        """Проверяет, истекла ли бронь"""
        return self.status == 'awaiting' and timezone.now() > self.expires_at

    def expire_if_needed(self):
        """Автоматически меняет статус на expired, если время вышло"""
        if self.is_expired():
            self.status = 'expired'
            self.save(update_fields=['status'])
            return True
        return False