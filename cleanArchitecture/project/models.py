"""
Models for Django app registration
Import ORM models from infrastructure layer
"""
from project.infrastructure.orm.models import (
    CustomerModel,
    BookModel,
    CartModel,
    CartItemModel
)

# Re-export for Django admin and migrations
Customer = CustomerModel
Book = BookModel
Cart = CartModel
CartItem = CartItemModel
