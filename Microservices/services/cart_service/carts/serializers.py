from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'book_id', 'quantity', 'created_at']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'customer_id', 'items', 'created_at', 'updated_at']


class AddToCartSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)
