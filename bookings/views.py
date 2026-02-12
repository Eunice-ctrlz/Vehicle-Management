from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from .models import Booking
from fleet.models import Car
from django.contrib import messages

@login_required 
def create_booking(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == "POST":
        pickup_str = request.POST.get('pickup_date')
        return_str = request.POST.get('return_date')
        
        
        pickup_date = parse_datetime(pickup_str)
        return_date = parse_datetime(return_str)
        
        
        duration = return_date - pickup_date
        days = int(duration.total_seconds() / 86400) + (1 if duration.total_seconds() % 86400 > 0 else 0)
        
        
        total_price = days * car.daily_rate
        
        Booking.objects.create(
            customer=request.user,
            car=car,
            pickup_date=pickup_date,
            return_date=return_date,
            total_price=total_price, 
            status='pending'
        )
        return redirect('my_bookings')

    return render(request, 'booking_form.html', {'car': car})

@login_required
def my_bookings(request):
    
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    # Ensure the booking exists and belongs to the logged-in user
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, "Your booking has been cancelled.")
    else:
        messages.error(request, "This booking cannot be cancelled as it is already confirmed or completed.")
    
    return redirect('my_bookings')