"""
Django ORM Models - Maps to MySQL database tables
"""
from django.db import models


class CustomerModel(models.Model):
    """Django ORM model for customers table"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customers'
        managed = False  # Table managed by SQL script

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        """Lưu mật khẩu plain text (không mã hóa)"""
        self.password = raw_password

    def check_password(self, raw_password):
        """So sánh mật khẩu plain text"""
        return self.password == raw_password


class BookModel(models.Model):
    """Django ORM model for books table"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'books'
        managed = False

    def __str__(self):
        return self.title


class CartModel(models.Model):
    """Django ORM model for carts table"""
    id = models.AutoField(primary_key=True)
    customer = models.OneToOneField(
        CustomerModel,
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


class CartItemModel(models.Model):
    """Django ORM model for cart_items table"""
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(
        CartModel,
        on_delete=models.CASCADE,
        db_column='cart_id',
        related_name='items'
    )
    book = models.ForeignKey(
        BookModel,
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
        return self.book.price * self.quantity
