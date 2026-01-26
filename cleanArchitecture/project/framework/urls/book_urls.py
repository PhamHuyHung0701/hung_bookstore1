"""
Book URLs
"""
from django.urls import path
from ..views import book_views

app_name = 'book'

urlpatterns = [
    path('', book_views.catalog, name='catalog'),
    path('<int:book_id>/', book_views.book_detail, name='detail'),
    path('add_stock/', book_views.add_stock, name='add_stock'),
    path('recommendations/', book_views.recommendations, name='recommendations'),
]
