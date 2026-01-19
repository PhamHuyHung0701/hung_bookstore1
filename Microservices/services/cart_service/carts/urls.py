from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('<int:customer_id>/', views.get_cart, name='get_cart'),
    path('<int:customer_id>/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('<int:customer_id>/clear/', views.clear_cart, name='clear_cart'),
]
