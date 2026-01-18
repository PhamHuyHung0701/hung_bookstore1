"""
Cart and CartItem Entities - Core business objects
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from .book import Book


@dataclass
class CartItem:
    """CartItem entity representing an item in the cart"""
    id: Optional[int] = None
    cart_id: Optional[int] = None
    book: Optional[Book] = None
    book_id: Optional[int] = None
    quantity: int = 1
    added_at: Optional[datetime] = None

    def get_subtotal(self) -> Decimal:
        """Calculate subtotal for this item"""
        if self.book:
            return self.book.price * self.quantity
        return Decimal("0.00")

    def to_dict(self) -> dict:
        """Convert entity to dictionary"""
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'book_id': self.book_id,
            'book': self.book.to_dict() if self.book else None,
            'quantity': self.quantity,
            'subtotal': float(self.get_subtotal()),
            'added_at': self.added_at
        }


@dataclass
class Cart:
    """Cart entity representing a shopping cart"""
    id: Optional[int] = None
    customer_id: Optional[int] = None
    items: List[CartItem] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def get_total(self) -> Decimal:
        """Calculate total price of all items in cart"""
        return sum(item.get_subtotal() for item in self.items)

    def get_item_count(self) -> int:
        """Get total number of different items in cart"""
        return len(self.items)

    def get_total_quantity(self) -> int:
        """Get total quantity of all items"""
        return sum(item.quantity for item in self.items)

    def to_dict(self) -> dict:
        """Convert entity to dictionary"""
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'items': [item.to_dict() for item in self.items],
            'total': float(self.get_total()),
            'item_count': self.get_item_count(),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
