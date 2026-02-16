from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from fleet import views as fleet_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', fleet_views.car_list, name='home'),
    path('bookings/', include('bookings.urls', namespace='bookings')),
    

    path('bookings/', include('bookings.urls')),
    path('', include('fleet.urls')), 
    

    path('payments/', include('payments.urls', namespace='payments')),
    path('', include('fleet.urls', namespace='fleet')),

]

# This allows Django to serve the car and license images you upload
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)