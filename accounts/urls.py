from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path("", views.index_view, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_detail, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path("more-cars", views.more_cars_view, name='more-cars')
]