from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15)
    license_front = forms.ImageField(required=True)
    license_back = forms.ImageField(required=True)
    next_of_kin_name = forms.CharField(max_length=100)
    next_of_kin_phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('username', 'email', 'phone_number', 'license_front', 'license_back', 'next_of_kin_name', 'next_of_kin_phone')