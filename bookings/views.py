from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from decimal import Decimal
from datetime import datetime

from .models import Booking
from fleet.models import Car

@login_required 
def create_booking(request, car_id):
    car = get_object_or_404(Car, id=car_id, is_available=True)
    
    if request.method == "POST":
        pickup_str = request.POST.get('pickup_date')
        return_str = request.POST.get('return_date')
        
        try:
            # Convert string inputs to timezone-aware datetime objects
            pickup_date = timezone.make_aware(datetime.fromisoformat(pickup_str))
            return_date = timezone.make_aware(datetime.fromisoformat(return_str))
            
            # Validation Logic
            if pickup_date < timezone.now():
                messages.error(request, "Pickup date cannot be in the past.")
            elif return_date <= pickup_date:
                messages.error(request, "Return date must be after pickup date.")
            else:
                # Calculate Duration (Round up to the nearest day)
                duration = return_date - pickup_date
                days = duration.days
                # If there's more than an hour extra, charge a full day
                if duration.seconds > 3600: 
                    days += 1
                days = max(1, days)

                total_price = Decimal(days) * Decimal(car.daily_rate)

                # Create Booking
                Booking.objects.create(
                    customer=request.user,
                    car=car,
                    pickup_date=pickup_date,
                    return_date=return_date,
                    total_price=total_price,
                    status='pending'
                )

                # Optional: Mark car as unavailable immediately
                car.is_available = False
                car.save()

                messages.success(request, f"Reservation for {car.name} submitted for review.")
                return redirect('bookings:my_bookings')

        except (ValueError, TypeError):
            messages.error(request, "Invalid date format. Please use the date picker.")

    return render(request, 'bookings/booking_form.html', {'car': car})

@login_required
def my_bookings(request):
    """
    Categorizes bookings into Active, Upcoming, and Past for the Premium UI.
    """
    now = timezone.now()
    all_user_bookings = Booking.objects.filter(customer=request.user).select_related('car')

    # 1. Active: Currently in use
    active_bookings = all_user_bookings.filter(
        status='confirmed',
        pickup_date__lte=now,
        return_date__gte=now
    )

    # 2. Upcoming: Not yet started (Pending or Confirmed)
    upcoming_bookings = all_user_bookings.filter(
        pickup_date__gt=now
    ).exclude(status__in=['cancelled', 'completed'])

    # 3. History: Finished or Cancelled
    past_bookings = all_user_bookings.filter(
        return_date__lt=now
    ) | all_user_bookings.filter(status__in=['cancelled', 'completed'])

    context = {
        'active_bookings': active_bookings,
        'upcoming_bookings': upcoming_bookings.order_by('pickup_date'),
        'past_bookings': past_bookings.order_by('-return_date'),
    }
    return render(request, 'bookings/my_bookings.html', context)

@login_required
def cancel_booking(request, booking_id):
    """
    Allows users to cancel only if the booking is still pending.
    """
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save()
        
        # Release the car back to the fleet
        booking.car.is_available = True
        booking.car.save()
        
        messages.success(request, "Booking cancelled successfully.")
    else:
        messages.error(request, "Confirmed bookings cannot be cancelled online. Please contact support.")
    
    return redirect('bookings:my_bookings')