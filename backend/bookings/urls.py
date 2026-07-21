from django.urls import path
from . import views

urlpatterns = [
    path('bookings/', views.create_booking, name='create_booking'),
    path('bookings/<int:booking_id>/pay/', views.pay_booking, name='pay_booking'),
    path('bookings/<int:booking_id>/extend/', views.extend_booking, name='extend_booking'),
] 
