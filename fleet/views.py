from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Profile
from .models import Car, VehicleAssignment, ConditionReport, MechanicRequest
from .forms import ConditionReportForm, MechanicRequestForm


@csrf_exempt
def update_gps(request, car_id):
    if request.method == 'POST':
        car = Car.objects.get(id=car_id)
        car.latitude = request.POST.get('lat')
        car.longitude = request.POST.get('lng')
        car.save()
        return JsonResponse({'status': 'success'})


def car_list(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'fleet/home.html', {'cars': cars})


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'fleet/car_detail.html', {'car': car})


@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    assignment = VehicleAssignment.objects.filter(profile=profile, is_active=True).first()
    return render(request, 'fleet_management/dashboard.html', {
        'profile': profile,
        'assignment': assignment
    })


@login_required
def post_condition_report(request):
    profile = Profile.objects.get(user=request.user)
    assignment = VehicleAssignment.objects.filter(profile=profile, is_active=True).first()

    if not assignment:
        messages.error(request, 'You have no assigned vehicle.')
        return redirect('dashboard')

    form = ConditionReportForm()
    if request.method == 'POST':
        form = ConditionReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.profile = profile
            report.car = assignment.car
            report.save()
            messages.success(request, 'Condition report submitted successfully.')
            return redirect('dashboard')

    return render(request, 'fleet_management/post_condition.html', {'form': form})


@login_required
def request_mechanic(request):
    profile = Profile.objects.get(user=request.user)
    assignment = VehicleAssignment.objects.filter(profile=profile, is_active=True).first()

    if not assignment:
        messages.error(request, 'You have no assigned vehicle.')
        return redirect('dashboard')

    form = MechanicRequestForm()
    if request.method == 'POST':
        form = MechanicRequestForm(request.POST)
        if form.is_valid():
            mechanic_request = form.save(commit=False)
            mechanic_request.profile = profile
            mechanic_request.car = assignment.car
            mechanic_request.save()
            messages.success(request, 'Mechanic request submitted successfully.')
            return redirect('dashboard')

    return render(request, 'fleet_management/request_mechanic.html', {'form': form})


@login_required
def my_reports(request):
    profile = Profile.objects.get(user=request.user)
    reports = ConditionReport.objects.filter(profile=profile).order_by('-reported_at')
    return render(request, 'fleet_management/my_reports.html', {'reports': reports})



# ADD THIS TO YOUR EXISTING views.py (fleet_management/views.py)

@login_required
def customer_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    
    # Active bookings
    active_bookings = VehicleAssignment.objects.filter(
        profile=profile,
        is_active=True
    ).select_related('car')
    
    # Past bookings
    past_bookings = VehicleAssignment.objects.filter(
        profile=profile,
        is_active=False
    ).select_related('car').order_by('-return_date')[:5]
    
    # Available cars
    available_cars = Car.objects.filter(
        is_available=True,
        status='available'
    )[:6]
    
    # Stats
    total_bookings = VehicleAssignment.objects.filter(profile=profile).count()
    pending_requests = MechanicRequest.objects.filter(profile=profile, status='pending').count()
    
    context = {
        'profile': profile,
        'active_bookings': active_bookings,
        'past_bookings': past_bookings,
        'available_cars': available_cars,
        'total_bookings': total_bookings,
        'pending_requests': pending_requests,
    }
    
    return render(request, 'fleet/customer_dashboard.html', context)