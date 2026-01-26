from django.db import models


class Cart(models.Model):
    """Cart model - maps to 'carts' table"""
    customer_id = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f"Cart #{self.id} - Customer #{self.customer_id}"


class CartItem(models.Model):
    """CartItem model - maps to 'cart_items' table"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book_id = models.IntegerField()
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'cart_items'

    def __str__(self):
        return f"CartItem #{self.id} - Book #{self.book_id} x {self.quantity}"


class Order(models.Model):
    """Order model"""
    customer_id = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"Order #{self.id} - Customer #{self.customer_id}"


class OrderItem(models.Model):
    """OrderItem model"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book_id = models.IntegerField()
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'order_items'

    def __str__(self):
        return f"OrderItem #{self.id} - Book #{self.book_id} x {self.quantity}"


class Shipping(models.Model):
    """Shipping model"""
    method_name = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'shipping'

    def __str__(self):
        return self.method_name


class Payment(models.Model):
    """Payment model"""
    method_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='pending')

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return self.method_name
