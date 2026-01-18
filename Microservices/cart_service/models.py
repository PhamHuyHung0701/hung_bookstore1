"""
Cart Service Models
"""
from django.db import models


class Cart(models.Model):
    """Cart model for cart_service"""
    id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField(unique=True)  # Reference to customer in customer_service
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'
        managed = False

    def __str__(self):
        return f"Cart of customer {self.customer_id}"


class CartItem(models.Model):
    """CartItem model for cart_service"""
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        db_column='cart_id',
        related_name='items'
    )
    book_id = models.IntegerField()  # Reference to book in book_service
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart_items'
        managed = False
        unique_together = ('cart', 'book_id')

    def __str__(self):
        return f"{self.quantity} x Book {self.book_id}"
