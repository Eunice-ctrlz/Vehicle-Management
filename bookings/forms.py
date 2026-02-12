from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['pickup_date', 'return_date']
        widgets = {

            'pickup_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'return_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }