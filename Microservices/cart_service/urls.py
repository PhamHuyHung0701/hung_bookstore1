"""
Cart Service URLs
"""
from django.urls import path
from . import views

app_name = 'cart_service'

urlpatterns = [
    path('<int:customer_id>/', views.get_cart, name='get_cart'),
    path('<int:customer_id>/add/', views.add_to_cart, name='add_to_cart'),
    path('<int:customer_id>/items/<int:item_id>/', views.update_cart_item, name='update_item'),
    path('<int:customer_id>/items/<int:item_id>/remove/', views.remove_from_cart, name='remove_item'),
    path('<int:customer_id>/clear/', views.clear_cart, name='clear_cart'),
]
