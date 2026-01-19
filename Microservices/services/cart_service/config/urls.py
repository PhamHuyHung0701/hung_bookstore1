from django.urls import path, include

urlpatterns = [
    path('api/cart/', include('carts.urls')),
]
