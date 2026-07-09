from django.contrib import admin
from .models import Hall, Row, Seat, Session


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['number', 'name']
    ordering = ['number']


@admin.register(Row)
class RowAdmin(admin.ModelAdmin):
    list_display = ['number', 'hall']
    list_filter = ['hall']
    ordering = ['hall', 'number']


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['number', 'row', 'type', 'price']
    list_filter = ['row__hall', 'type']
    ordering = ['row', 'number']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'hall', 'started_at', 'duration']
    list_filter = ['hall', 'started_at']
    ordering = ['started_at']
    date_hierarchy = 'started_at'