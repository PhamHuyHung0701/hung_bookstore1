"""
Book URLs
"""
from django.urls import path
from ..views import book_views

app_name = 'book'

urlpatterns = [
    path('', book_views.catalog, name='catalog'),
    path('<int:book_id>/', book_views.book_detail, name='detail'),
]
