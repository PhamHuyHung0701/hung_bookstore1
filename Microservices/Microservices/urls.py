"""
URL configuration for Microservices project.

Main URL router that combines:
- API endpoints for each microservice
- Web gateway for frontend
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints for microservices
    path('api/customers/', include('customer_service.urls')),
    path('api/books/', include('book_service.urls')),
    path('api/cart/', include('cart_service.urls')),
    
    # Web frontend via API Gateway
    path('', include('api_gateway.urls')),
]
