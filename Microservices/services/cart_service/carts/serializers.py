from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem, Shipping, Payment


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'book_id', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'customer_id', 'is_active', 'items']


class AddToCartSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'total_price', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'book_id', 'quantity']


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['id', 'method_name', 'fee']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'method_name', 'status']


class CheckoutSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    shipping_id = serializers.IntegerField()
    payment_id = serializers.IntegerField()
