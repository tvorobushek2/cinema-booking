from django.urls import path
from . import views

urlpatterns = [
    path('sessions/', views.SessionListView.as_view(), name='session-list'),
    path('sessions/<int:pk>/seats/', views.SessionSeatsView.as_view(), name='session-seats'),
]