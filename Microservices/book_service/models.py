"""
Book Service Models
"""
from django.db import models


class Book(models.Model):
    """Book model for book_service"""
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

    def is_available(self):
        return self.stock > 0

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'price': float(self.price),
            'stock': self.stock,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
