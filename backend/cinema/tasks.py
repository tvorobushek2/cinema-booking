from celery import shared_task
from django.utils import timezone
from .models import Booking


@shared_task
def expire_old_bookings():
    """
    Фоновая задача для очистки истекших броней
    Запускается каждые 5 минут
    """
    now = timezone.now()
    
    expired_bookings = Booking.objects.filter(
        status='awaiting',
        expires_at__lt=now
    )
    
    count = expired_bookings.update(status='expired')
    
    if count > 0:
        from django.core.cache import cache
        cache.delete('sessions_list')
    
    return f'Expired {count} bookings'