"""
API Gateway URLs
"""
from django.urls import path
from . import views

app_name = 'gateway'

urlpatterns = [
    # Customer routes
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Book routes
    path('', views.catalog, name='catalog'),
    path('books/', views.catalog, name='books'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    
    # Cart routes
    path('cart/', views.view_cart, name='cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
