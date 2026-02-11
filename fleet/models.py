from django.db import models

# Create your models here.
from django.db import models

class Car(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('maintenance', 'In Maintenance'),
    ]

    name = models.CharField(max_length=100, help_text="e.g. Toyota Prado")
    plate_number = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='cars/')
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    description = models.TextField(blank=True, null=True)


    # GPS Tracking
    latitude = models.FloatField(default=-1.286389) # Nairobi center
    longitude = models.FloatField(default=36.817223)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.plate_number}"
    