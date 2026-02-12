from django.contrib import admin

# Register your models here.
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'car', 'pickup_date', 'return_date', 'total_price', 'created_at')
    search_fields = ('customer__username', 'car__name')
    list_filter = ('pickup_date', 'return_date')

    actions = ['mark_as_confirmed', 'mark_as_completed']

    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = "Confirm selected bookings"