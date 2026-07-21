 
from celery import shared_task
from django.db import transaction
from django.utils import timezone
from .models import Booking
import logging

logger = logging.getLogger(__name__)

@shared_task
def expire_old_bookings():
    now = timezone.now()
    with transaction.atomic():
        expired_bookings = Booking.objects.filter(
            status='awaiting',
            expires_at__lte=now
        ).select_for_update()

        count = expired_bookings.count()
        if count > 0:
            expired_bookings.update(status='expired')
            logger.info(f"✅ Истекло и освобождено {count} мест(а)")
            ids = list(expired_bookings.values_list('id', flat=True))
            logger.info(f"Освобождены брони ID: {ids}")
        else:
            logger.debug("Нет истекших бронирований")
        return f"Processed {count} expired bookings"