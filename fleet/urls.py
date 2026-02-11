from django.urls import path
from . import views

app_name = 'fleet'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('condition-report/', views.post_condition_report, name='post_condition_report'),
    path('request-mechanic/', views.request_mechanic, name='request_mechanic'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    path('update-gps/<int:car_id>/', views.update_gps, name='update_gps'),
    path('customer-dashboad/', views.customer_dashboard, name='customer-dashboard'),
]