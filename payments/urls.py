from django.urls import path
from . import views

urlpatterns = [
    path('pay/<int:booking_id>/', views.process_payment, name='process_payment'),
    path('callback/', views.mpesa_callback, name='mpesa_callback'),
    path('check-status/<int:checkout_id>/', views.check_payment_status, name='check_status'),
]