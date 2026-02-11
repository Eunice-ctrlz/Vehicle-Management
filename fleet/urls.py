from django.contrib import admin
from django.urls import path, include
from fleet import views as fleet_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('accounts/', include('accounts.urls')),
    path('', fleet_views.car_list, name='home'), 
    path('car/<int:pk>/', fleet_views.car_detail, name='car_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)