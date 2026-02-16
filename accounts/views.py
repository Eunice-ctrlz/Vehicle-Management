
from django.shortcuts import redirect, render
from .forms import UserRegistrationForm
from django.contrib import messages
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES) # request.FILES is crucial!
        if form.is_valid():
            user = form.save()
            # Update the automatically created profile with the extra form data
            profile = user.profile
            profile.phone_number = form.cleaned_data['phone_number']
            profile.license_front = form.cleaned_data['license_front']
            profile.license_back = form.cleaned_data['license_back']
            profile.next_of_kin_name = form.cleaned_data['next_of_kin_name']
            profile.next_of_kin_phone = form.cleaned_data['next_of_kin_phone']
            profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {user.username}! You can login')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

