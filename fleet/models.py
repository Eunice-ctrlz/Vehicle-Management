from django.db import models
from accounts.models import Profile


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
    latitude = models.FloatField(default=-1.286389)
    longitude = models.FloatField(default=36.817223)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.plate_number}"


class VehicleAssignment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.profile.user.username} - {self.car}"


class ConditionReport(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    description = models.TextField()
    photo = models.ImageField(upload_to='condition_photos/', blank=True, null=True)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.profile.user.username} on {self.reported_at}"


class MechanicRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    issue_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request by {self.profile.user.username} - {self.status}"