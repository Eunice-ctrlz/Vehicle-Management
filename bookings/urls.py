from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:car_id>/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'), 
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]