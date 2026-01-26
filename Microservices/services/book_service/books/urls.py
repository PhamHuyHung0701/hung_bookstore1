from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_books, name='list_books'),
    path('add/', views.add_book, name='add_book'),
    path('<int:book_id>/', views.get_book, name='get_book'),
    path('<int:book_id>/stock/', views.check_stock, name='check_stock'),
    path('<int:book_id>/update-stock/', views.update_stock, name='update_stock'),
    path('recommendations/', views.get_recommendations, name='get_recommendations'),
    path('staff/login/', views.staff_login, name='staff_login'),
]
