from django.urls import path
from . import views

app_name = 'book'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('<int:book_id>/', views.book_detail, name='detail'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('recommendations/', views.recommendations, name='recommendations'),
]
