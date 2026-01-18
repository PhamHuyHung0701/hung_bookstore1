"""
Customer Service URLs
"""
from django.urls import path
from . import views

app_name = 'customer_service'

urlpatterns = [
    path('', views.list_customers, name='list'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('<int:customer_id>/', views.get_customer, name='detail'),
    path('<int:customer_id>/exists/', views.check_customer_exists, name='exists'),
]
