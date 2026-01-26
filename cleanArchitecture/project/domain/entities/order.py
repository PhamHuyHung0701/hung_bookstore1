"""
Order and OrderItem Entities - Core business objects
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from .book import Book


@dataclass
class OrderItem:
    """OrderItem entity representing an item in an order"""
    id: Optional[int] = None
    order_id: Optional[int] = None
    book: Optional[Book] = None
    book_id: Optional[int] = None
    quantity: int = 1
    price: Decimal = Decimal("0.00")

    def get_subtotal(self) -> Decimal:
        """Calculate subtotal for this item"""
        return self.price * self.quantity

    def to_dict(self) -> dict:
        """Convert entity to dictionary"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'book_id': self.book_id,
            'book': self.book.to_dict() if self.book else None,
            'quantity': self.quantity,
            'price': float(self.price),
            'subtotal': float(self.get_subtotal())
        }


@dataclass
class Order:
    """Order entity representing a customer order"""
    id: Optional[int] = None
    customer_id: Optional[int] = None
    total_price: Decimal = Decimal("0.00")
    shipping_id: Optional[int] = None
    payment_id: Optional[int] = None
    created_at: Optional[datetime] = None
    items: List[OrderItem] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert entity to dictionary"""
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'total_price': float(self.total_price),
            'shipping_id': self.shipping_id,
            'payment_id': self.payment_id,
            'created_at': self.created_at,
            'items': [item.to_dict() for item in self.items]
        }
