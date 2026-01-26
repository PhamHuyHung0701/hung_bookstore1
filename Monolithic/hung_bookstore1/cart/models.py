from django.db import models
from hung_bookstore1.customer.models import Customer
from hung_bookstore1.book.models import Book


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        db_column='customer_id'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f"Cart of {self.customer.name}"

    def get_total(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.book.price * item.quantity
        return total


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        db_column='cart_id'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        db_column='book_id'
    )
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'cart_items'
        unique_together = ('cart', 'book')

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"

    def get_subtotal(self):
        return self.book.price * self.quantity


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    shipping = models.ForeignKey('Shipping', null=True, blank=True, on_delete=models.SET_NULL)
    payment = models.ForeignKey('Payment', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"Order #{self.id} - {self.customer.email}"


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_items'

    def subtotal(self):
        return self.price * self.quantity


class Shipping(models.Model):
    id = models.AutoField(primary_key=True)
    method_name = models.CharField(max_length=120)
    fee = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'shipping'

    def __str__(self):
        return f"{self.method_name} ({self.fee})"


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    method_name = models.CharField(max_length=120)
    status = models.CharField(max_length=50, default='pending')

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return f"{self.method_name} - {self.status}"
