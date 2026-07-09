from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from cinema.models import Hall, Row, Seat, Session


class Command(BaseCommand):
    help = 'Наполняет базу тестовыми данными (залы, ряды, места, сеансы)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🎬 Начинаем наполнение базы...'))

        # Очищаем старые данные
        Session.objects.all().delete()
        Seat.objects.all().delete()
        Row.objects.all().delete()
        Hall.objects.all().delete()
        self.stdout.write(self.style.WARNING('🗑 Старые данные удалены'))

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
            for row_num in range(1, 6):  # 5 рядов
                row = Row.objects.create(hall=hall, number=row_num)
                
                for seat_num in range(1, 9):  # 8 мест в ряду
                    # Каждое 3-е место — VIP
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

        # Создаем 5 сеансов на ближайшие дни
        now = timezone.now()
        movies = [
            ('Дюна: Часть вторая', 166),
            ('Оппенгеймер', 180),
            ('Барби', 114),
            ('Человек-паук: Паутина вселенных', 140),
            ('Миссия невыполнима: Смертельная расплата', 163),
        ]

        sessions = []
        for i, (title, duration) in enumerate(movies):
            hall = halls[i % len(halls)]  # Чередруем залы
            start_time = now + timedelta(days=i, hours=18, minutes=0)
            
            sessions.append(Session(
                hall=hall,
                title=title,
                started_at=start_time,
                duration=duration
            ))

        Session.objects.bulk_create(sessions)
        self.stdout.write(self.style.SUCCESS(f'✅ Создано {len(sessions)} сеансов'))

        # Итоговая статистика
        self.stdout.write(self.style.SUCCESS('\n📊 Статистика:'))
        self.stdout.write(f'  Залов: {Hall.objects.count()}')
        self.stdout.write(f'  Рядов: {Row.objects.count()}')
        self.stdout.write(f'  Мест: {Seat.objects.count()}')
        self.stdout.write(f'  Сеансов: {Session.objects.count()}')
        self.stdout.write(self.style.SUCCESS('\n🎉 Готово! Откройте http://localhost:8000/admin/'))