from django.contrib import admin
from django.utils import timezone
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # What you see in the main list
    list_display = ('booking_reference', 'customer', 'car', 'status', 'pickup_date', 'total_price', 'is_active_now')
    list_filter = ('status', 'created_at', 'pickup_date')
    search_fields = ('booking_reference', 'customer__username', 'car__name')
    readonly_fields = ('booking_reference', 'created_at', 'total_price')
    
    # Custom Actions
    actions = ['confirm_bookings', 'complete_bookings', 'cancel_bookings']

    def is_active_now(self, obj):
        return obj.is_active
    is_active_now.boolean = True
    is_active_now.short_description = "Live HUD Active"

    @admin.action(description="Confirm selected bookings (Locks Cars)")
    def confirm_bookings(self, request, queryset):
        for booking in queryset:
            booking.status = 'confirmed'
            booking.save()
            # Mark the car as unavailable when confirmed
            booking.car.is_available = False
            booking.car.save()
        self.message_user(request, f"{queryset.count()} bookings confirmed and cars locked.")

    @admin.action(description="Complete selected bookings (Releases Cars)")
    def complete_bookings(self, request, queryset):
        for booking in queryset:
            booking.status = 'completed'
            booking.save()
            # Make car available again
            booking.car.is_available = True
            booking.car.save()
        self.message_user(request, f"{queryset.count()} bookings completed. Cars are now back in fleet.")

    @admin.action(description="Cancel selected bookings")
    def cancel_bookings(self, request, queryset):
        for booking in queryset:
            booking.status = 'cancelled'
            booking.save()
            booking.car.is_available = True
            booking.car.save()
        self.message_user(request, f"{queryset.count()} bookings cancelled.")