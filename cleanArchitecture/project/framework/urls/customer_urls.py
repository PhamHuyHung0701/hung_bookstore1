"""
Customer URLs
"""
from django.urls import path
from ..views import customer_views

app_name = 'customer'

urlpatterns = [
    path('register/', customer_views.register, name='register'),
    path('login/', customer_views.login, name='login'),
    path('logout/', customer_views.logout, name='logout'),
    path('profile/', customer_views.profile, name='profile'),
    path('staff-login/', customer_views.staff_login, name='staff_login'),
    path('staff-logout/', customer_views.staff_logout, name='staff_logout'),
]
