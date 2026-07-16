from django.urls import path
from . import views

urlpatterns = [
    path('sessions/', views.SessionListView.as_view(), name='session-list'),
    path('sessions/<int:pk>/seats/', views.SessionSeatsView.as_view(), name='session-seats'),
    path('bookings/', views.BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/pay/', views.BookingPayView.as_view(), name='booking-pay'),
    path('bookings/<int:pk>/extend/', views.BookingExtendView.as_view(), name='booking-extend'),
]