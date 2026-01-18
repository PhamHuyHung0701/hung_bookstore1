"""
Cart Service Serializers
"""
from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart_id', 'book_id', 'book', 'quantity', 'subtotal', 'added_at']
        read_only_fields = ['id', 'added_at']

    def get_book(self, obj):
        """Get book data from book_service"""
        from .service_client import ServiceClient
        return ServiceClient.get_book(obj.book_id)

    def get_subtotal(self, obj):
        """Calculate subtotal"""
        from .service_client import ServiceClient
        book = ServiceClient.get_book(obj.book_id)
        if book:
            return float(book['price']) * obj.quantity
        return 0


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'customer_id', 'customer', 'items', 'total', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_total(self, obj):
        """Calculate total price of all items"""
        total = 0
        from .service_client import ServiceClient
        for item in obj.items.all():
            book = ServiceClient.get_book(item.book_id)
            if book:
                total += float(book['price']) * item.quantity
        return total

    def get_customer(self, obj):
        """Get customer data from customer_service"""
        from .service_client import ServiceClient
        return ServiceClient.get_customer(obj.customer_id)


class AddToCartSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=0)
