from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'plate_number', 'is_available', 'last_updated', 'status')
    search_fields = ('name', 'plate_number')
    
    # This organizes the car info into sections
    fieldsets = (
        ('Vehicle Info', {
            'fields': ('name', 'brand', 'plate_number', 'image', 'daily_rate', 'status', 'is_available', 'description')
        }),
        ('Location Settings', {
            'fields': ('latitude', 'longitude'),
            'description': "Drag the marker on the map above to set coordinates."
        }),
    )

    
    class Media:
        css = {
            'all': ('https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',)
        }
        js = (
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
            'admin_map.js', 
        )