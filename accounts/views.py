from django.shortcuts import redirect, render
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                role='customer',
                phone_number=form.cleaned_data['phone_number'],
                next_of_kin_name=form.cleaned_data['next_of_kin_name'],
                next_of_kin_phone=form.cleaned_data['next_of_kin_phone']
)
            messages.success(request, f'Account created for {user.username}! You can login')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            profile = Profile.objects.get(user=user)
            if profile.role == 'driver':
                return redirect('dashboard')
            else:
                return redirect('fleet:customer-dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def profile_detail(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'accounts/profile_detail.html', {'profile': profile})


@login_required
def profile_update(request):
    profile, = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        profile.phone_number = request.POST.get('phone_number')
        profile.next_of_kin_name = request.POST.get('next_of_kin_name')
        profile.next_of_kin_phone = request.POST.get('next_of_kin_phone')
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile_detail')

    return render(request, 'accounts/profile_update.html', {'profile': profile})




def index_view(request):
    return render(request, 'accounts/index.html')

def more_cars_view(request):
    return render(request, 'accounts/more_cars.html')


