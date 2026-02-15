from django.urls import path
from . import views

app_name = 'payments'
urlpatterns = [
    path('pay/<int:booking_id>/', views.process_payment, name='process_payment'),
    path('callback/', views.mpesa_callback, name='mpesa_callback'),
    path('check-status/<str:checkout_id>/', views.check_payment_status, name='check_status'),
]