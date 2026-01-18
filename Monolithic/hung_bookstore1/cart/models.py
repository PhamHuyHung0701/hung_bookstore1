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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'
        managed = False

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
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart_items'
        managed = False
        unique_together = ('cart', 'book')

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"

    def get_subtotal(self):
        """Tính thành tiền cho item này"""
        return self.book.price * self.quantity
