"""
Book Service URLs
"""
from django.urls import path
from . import views

app_name = 'book_service'

urlpatterns = [
    path('', views.list_books, name='list'),
    path('<int:book_id>/', views.get_book, name='detail'),
    path('<int:book_id>/stock/', views.check_book_stock, name='stock'),
    path('<int:book_id>/update-stock/', views.update_stock, name='update_stock'),
    path('<int:book_id>/exists/', views.check_book_exists, name='exists'),
]
