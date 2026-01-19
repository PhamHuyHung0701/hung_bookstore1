from django.db import models


class Cart(models.Model):
    """Cart model - maps to 'carts' table"""
    customer_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f"Cart #{self.id} - Customer #{self.customer_id}"


class CartItem(models.Model):
    """CartItem model - maps to 'cart_items' table"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book_id = models.IntegerField()
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart_items'

    def __str__(self):
        return f"CartItem #{self.id} - Book #{self.book_id} x {self.quantity}"
