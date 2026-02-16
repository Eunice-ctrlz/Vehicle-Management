from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Import your car list view directly to use as the home page
from fleet.views import car_list 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. THE HOME PAGE (Explicitly defined first)
    path('', car_list, name='home'), 

    # 2. THE APPS
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('bookings/', include('bookings.urls', namespace='bookings')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('fleet/', include('fleet.urls', namespace='fleet')), # Moved to /fleet/
]

# 3. STATIC/MEDIA (Only at the very end)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)