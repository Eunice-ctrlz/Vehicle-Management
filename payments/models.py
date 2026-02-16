from django.db import models

# Create your models here.
from bookings.models import Booking

class MpesaTransaction(models.Model):
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    checkout_request_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending') 
    receipt_number = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.amount} - {self.status}"