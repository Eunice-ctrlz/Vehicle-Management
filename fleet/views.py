from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

# Model Imports
from accounts.models import Profile
from bookings.models import Booking
from .models import Car, VehicleAssignment, ConditionReport, MechanicRequest
from .forms import ConditionReportForm, MechanicRequestForm


def home(request):
    query = request.GET.get('q')
    max_price = request.GET.get('price')
    cars = Car.objects.filter(is_available=True)

    if query:
        # Search by brand or car name
        cars = cars.filter(name__icontains=query) | cars.filter(brand__icontains=query)
    
    if max_price:
        # Filter by daily rate
        cars = cars.filter(daily_rate__lte=max_price)

    return render(request, 'fleet/home.html', {'cars': cars})


# --- GPS TRACKING ---

@csrf_exempt
def update_gps(request, car_id):
    if request.method == 'POST':
        car = get_object_or_404(Car, id=car_id)
        car.latitude = request.POST.get('lat')
        car.longitude = request.POST.get('lng')
        car.save()
        return JsonResponse({'status': 'success'})

# --- PUBLIC VIEWS ---
def car_list(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'fleet/home.html', {'cars': cars})

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'fleet/car_detail.html', {'car': car})

# --- CUSTOMER DASHBOARD ---
@login_required
def customer_dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    
    user_bookings = Booking.objects.filter(customer=request.user)
    
    
    active_bookings = user_bookings.filter(
        status__in=['pending', 'confirmed']
    ).select_related('car').order_by('-created_at') 
    
    
    context = {
        'profile': profile,
        'active_bookings': active_bookings,
        'available_cars': Car.objects.filter(is_available=True)[:6],
        'total_bookings': user_bookings.count(),
    }
    return render(request, 'fleet/customer_dashboard.html', context)

# --- BOOKING LOGIC ---
@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if not car.is_available:
        messages.error(request, "Sorry, this car is currently unavailable.")
        return redirect('fleet:customer-dashboard')

    # FIXED: Use 'customer' instead of 'user'
    # FIXED: Use 'pending' (lowercase) to match your dashboard filters
    Booking.objects.create(
        customer=request.user,
        car=car,
        status='pending',
        pickup_date=timezone.now() # Use the field name from your model
    )
    
    car.is_available = False
    car.save()
    
    messages.success(request, f"You have successfully rented the {car.name}!")
    return redirect('fleet:customer-dashboard')

# --- PAYMENT LOGIC ---
@login_required
def create_payment(request, booking_id):
    """
    Handles the 'Pay Now' button logic.
    """
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    # Logic to process payment (Placeholder for M-Pesa/Stripe)
    booking.is_paid = True
    booking.save()
    
    messages.success(request, f"Payment for {booking.car.name} received successfully.")
    return redirect('fleet:customer-dashboard')

# --- FLEET MANAGEMENT (ASSIGNMENTS & REPORTS) ---
@login_required
def post_condition_report(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    # Check for active assignments
    assignment = VehicleAssignment.objects.filter(profile=profile, is_active=True).first()

    if not assignment:
        messages.error(request, 'You have no assigned vehicle to report on.')
        return redirect('fleet:customer-dashboard')

    if request.method == 'POST':
        form = ConditionReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.profile = profile
            report.car = assignment.car
            report.save()
            messages.success(request, 'Condition report submitted successfully.')
            return redirect('fleet:customer-dashboard')
    else:
        form = ConditionReportForm()
    return render(request, 'fleet_management/post_condition.html', {'form': form})

@login_required
def request_mechanic(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    assignment = VehicleAssignment.objects.filter(profile=profile, is_active=True).first()

    if not assignment:
        messages.error(request, 'No active vehicle assignment found.')
        return redirect('fleet:customer-dashboard')

    if request.method == 'POST':
        form = MechanicRequestForm(request.POST)
        if form.is_valid():
            mechanic_request = form.save(commit=False)
            mechanic_request.profile = profile
            mechanic_request.car = assignment.car
            mechanic_request.save()
            messages.success(request, 'Mechanic request sent.')
            return redirect('fleet:customer-dashboard')
    else:
        form = MechanicRequestForm()
    return render(request, 'fleet_management/request_mechanic.html', {'form': form})