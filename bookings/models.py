import uuid
from django.db import models
from django.conf import settings
from fleet.models import Car

# Create your models here.
from django.conf import settings
from fleet.models import Car


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),

        ('active', 'Active'), 
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]


    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    pickup_date = models.DateTimeField()
    return_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.car.name}"

   
    booking_reference = models.CharField(max_length=12, 
                unique=True, editable=False, null=True, blank=True)
    
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    
    # Timing
    pickup_date = models.DateTimeField()
    return_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Financials
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        
        if not self.booking_reference:
            self.booking_reference = f"DF-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_reference} | {self.car.name} ({self.customer.username})"

    @property
    def duration_days(self):
        
        delta = self.return_date - self.pickup_date
        days = delta.days
       
        if delta.seconds > 3600: 
            days += 1
        return max(1, days)

    @property
    def is_active(self):
        """Helper to quickly check if the rental is currently happening"""
        from django.utils import timezone
        return self.status == 'confirmed' and self.pickup_date <= timezone.now() <= self.return_date

