"""
Cart URLs
"""
from django.urls import path
from ..views import cart_views

app_name = 'cart'

urlpatterns = [
    path('', cart_views.view_cart, name='view_cart'),
    path('add/<int:book_id>/', cart_views.add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', cart_views.update_cart_item, name='update_item'),
    path('remove/<int:item_id>/', cart_views.remove_from_cart, name='remove_item'),
]
