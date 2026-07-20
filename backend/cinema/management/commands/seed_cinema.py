from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from cinema.models import Hall, Row, Seat, Session


class Command(BaseCommand):
    help = 'Наполняет базу тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Начинаем наполнение базы...'))

        # Очищаем старые данные
        Session.objects.all().delete()
        Seat.objects.all().delete()
        Row.objects.all().delete()
        Hall.objects.all().delete()
        self.stdout.write(self.style.WARNING('Старые данные удалены'))

        # Создаем 3 зала
        halls = [
            Hall(number=1, name='IMAX'),
            Hall(number=2, name='Стандартный'),
            Hall(number=3, name='VIP'),
        ]
        Hall.objects.bulk_create(halls)
        self.stdout.write(self.style.SUCCESS(f'✅ Создано {len(halls)} зала'))

        # Для каждого зала создаем 5 рядов по 8 мест
        total_seats = 0
        for hall in halls:
            for row_num in range(1, 6):
                row = Row.objects.create(hall=hall, number=row_num)
                
                for seat_num in range(1, 9):
                    seat_type = 'vip' if seat_num % 3 == 0 else 'standard'
                    price = 500.00 if seat_type == 'vip' else 300.00
                    
                    Seat.objects.create(
                        row=row,
                        number=seat_num,
                        type=seat_type,
                        price=price
                    )
                    total_seats += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Создано {total_seats} мест'))

        # Создаем 5 сеансов с постерами
        now = timezone.now()
        movies = [
    ('Дюна: Часть вторая', 166, 'https://images-s.kinorium.com/movie/poster/2808886/w1500_52368132.jpg'),
    ('Оппенгеймер', 180, 'https://content.onliner.by/news/970x485/487e694bbe131ec2137dc0d9664241db.jpegr'),
    ('Барби', 114, 'https://beam-images.warnermediacdn.com/BEAM_LWM_DELIVERABLES/80bc4915-c826-499f-9961-b422b17559b6/84787bd6-df58-11f0-80ce-0affd03b90c7?host=wbd-images.prod-vod.h264.io&amp;partner=beamcom&amp;w=500'),
    ('Человек-паук: Паутина вселенных', 140, 'https://images-s.kinorium.com/movie/poster/2005077/w1500_51369915.jpg'),
    ('Миссия невыполнима: Смертельная расплата', 163, 'https://ru-images-s.kinorium.com/movie/1080/2016603.jpg?1693072045'),
]

        sessions = []
        for i, (title, duration, poster) in enumerate(movies):
            hall = halls[i % len(halls)]
            start_time = now + timedelta(days=i, hours=18)
            
            sessions.append(Session(
                hall=hall,
                title=title,
                poster=poster,
                started_at=start_time,
                duration=duration
            ))

        Session.objects.bulk_create(sessions)
        self.stdout.write(self.style.SUCCESS(f'✅ Создано {len(sessions)} сеансов'))

        # Очищаем кэш
        from django.core.cache import cache
        cache.clear()
        self.stdout.write(self.style.SUCCESS('️ Кэш очищен'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Готово!'))