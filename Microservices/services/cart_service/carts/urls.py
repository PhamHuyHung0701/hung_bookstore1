from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('<int:customer_id>/', views.get_cart, name='get_cart'),
    path('<int:customer_id>/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('<int:customer_id>/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('<int:customer_id>/clear/', views.clear_cart, name='clear_cart'),
    path('<int:customer_id>/orders/', views.get_order_history, name='get_order_history'),
    path('checkout/', views.checkout, name='checkout'),
    path('shipping/', views.get_shipping_options, name='get_shipping_options'),
    path('payment/', views.get_payment_options, name='get_payment_options'),
]
