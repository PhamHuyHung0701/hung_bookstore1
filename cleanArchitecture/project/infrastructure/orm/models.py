"""
Django ORM Models - Maps to SQLite database tables
"""
from django.db import models
from django.db.models import Avg


class CustomerModel(models.Model):
    """Django ORM model for customers table"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return self.name

    def check_password(self, raw_password):
        """So sánh mật khẩu plain text"""
        return self.password == raw_password


class BookModel(models.Model):
    """Django ORM model for books table"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'books'

    def __str__(self):
        return self.title

    def is_available(self):
        return self.stock_quantity > 0

    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return sum(r.score for r in ratings) / ratings.count()
        return 0

    @classmethod
    def recommend_for_customer(cls, customer_id, limit=5):
        """
        Simple recommendation:
        - Books the customer bought previously -> recommend similar authors
        - Or top-rated books overall
        """
        bought_authors = (
            cls.objects.filter(orderitem__order__customer_id=customer_id)
            .values_list('author', flat=True).distinct()
        )
        qs = cls.objects.none()
        if bought_authors:
            qs = cls.objects.filter(author__in=list(bought_authors)).order_by('-stock_quantity')
        if not qs.exists():
            qs = cls.objects.annotate(avg_rating=Avg('ratings__score')).order_by('-avg_rating')
        return qs[:limit]


class RatingModel(models.Model):
    """Django ORM model for ratings table"""
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE, related_name='ratings')
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField()

    class Meta:
        db_table = 'ratings'
        unique_together = ('customer', 'book')


class StaffModel(models.Model):
    """Django ORM model for staff table"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)

    class Meta:
        db_table = 'staff'

    def __str__(self):
        return f"{self.name} ({self.role})"


class CartModel(models.Model):
    """Django ORM model for carts table"""
    id = models.AutoField(primary_key=True)
    customer = models.OneToOneField(
        CustomerModel,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f"Cart of {self.customer.name}"

    def add_book(self, book, quantity=1):
        item, created = CartItemModel.objects.get_or_create(cart=self, book=book, defaults={'quantity': quantity})
        if not created:
            item.quantity += quantity
            item.save()
        return item

    def total_price(self):
        return sum(ci.subtotal() for ci in self.items.all())


class CartItemModel(models.Model):
    """Django ORM model for cart_items table"""
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(
        CartModel,
        on_delete=models.CASCADE,
        related_name='items'
    )
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'cart_items'
        unique_together = ('cart', 'book')

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"

    def subtotal(self):
        return self.book.price * self.quantity


class OrderModel(models.Model):
    """Django ORM model for orders table"""
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    shipping = models.ForeignKey('ShippingModel', null=True, blank=True, on_delete=models.SET_NULL)
    payment = models.ForeignKey('PaymentModel', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"Order #{self.id} - {self.customer.email}"


class OrderItemModel(models.Model):
    """Django ORM model for order_items table"""
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_items'

    def subtotal(self):
        return self.price * self.quantity


class ShippingModel(models.Model):
    """Django ORM model for shipping table"""
    id = models.AutoField(primary_key=True)
    method_name = models.CharField(max_length=120)
    fee = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'shipping'

    def __str__(self):
        return f"{self.method_name} ({self.fee})"


class PaymentModel(models.Model):
    """Django ORM model for payments table"""
    id = models.AutoField(primary_key=True)
    method_name = models.CharField(max_length=120)
    status = models.CharField(max_length=50, default='pending')

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return f"{self.method_name} - {self.status}"
