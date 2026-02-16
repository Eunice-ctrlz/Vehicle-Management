from django.contrib import admin
from django.utils import timezone
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # 1. Main List Display
    list_display = (
        'booking_reference', 
        'customer', 
        'car', 
        'status', 
        'pickup_date', 
        'total_price', 
        'is_active_now'
    )
    
    # 2. Sidebar Filters & Search
    list_filter = ('status', 'created_at', 'pickup_date')
    search_fields = ('booking_reference', 'customer__username', 'car__name')
    
    # 3. Form Layout Settings
    readonly_fields = ('booking_reference', 'created_at', 'total_price')
    
    # 4. Custom Actions for Fleet Management
    actions = ['confirm_bookings', 'complete_bookings', 'cancel_bookings']

    # Custom Column: Shows if the car is currently out with the customer
    def is_active_now(self, obj):
        now = timezone.now()
        return obj.status == 'confirmed' and obj.pickup_date <= now <= obj.return_date
    is_active_now.boolean = True
    is_active_now.short_description = "Live HUD Active"

    @admin.action(description="Confirm selected bookings (Locks Cars)")
    def confirm_bookings(self, request, queryset):
        for booking in queryset:
            booking.status = 'confirmed'
            booking.save()
            # Lock the car from other rentals
            booking.car.is_available = False
            booking.car.save()
        self.message_user(request, f"{queryset.count()} bookings confirmed and cars locked.")

    @admin.action(description="Complete selected bookings (Releases Cars)")
    def complete_bookings(self, request, queryset):
        for booking in queryset:
            booking.status = 'completed'
            booking.save()
            # Release the car back to the public fleet
            booking.car.is_available = True
            booking.car.save()
        self.message_user(request, f"{queryset.count()} bookings marked as completed.")

    @admin.action(description="Cancel selected bookings (Releases Cars)")
    def cancel_bookings(self, request, queryset):
        for booking in queryset:
            booking.status = 'cancelled'
            booking.save()
            # Ensure the car is available for someone else
            booking.car.is_available = True
            booking.car.save()
        self.message_user(request, f"{queryset.count()} bookings cancelled.")