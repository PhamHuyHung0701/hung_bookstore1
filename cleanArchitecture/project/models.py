"""
Models for Django app registration
Import ORM models from infrastructure layer
"""
from project.infrastructure.orm.models import (
    CustomerModel,
    BookModel,
    CartModel,
    CartItemModel,
    RatingModel,
    StaffModel,
    OrderModel,
    OrderItemModel,
    ShippingModel,
    PaymentModel
)

# Re-export for Django admin and migrations
Customer = CustomerModel
Book = BookModel
Cart = CartModel
CartItem = CartItemModel
Rating = RatingModel
Staff = StaffModel
Order = OrderModel
OrderItem = OrderItemModel
Shipping = ShippingModel
Payment = PaymentModel
