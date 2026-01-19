from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_customers, name='list_customers'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('<int:customer_id>/', views.get_customer, name='get_customer'),
    path('<int:customer_id>/exists/', views.check_customer_exists, name='check_customer_exists'),
]
