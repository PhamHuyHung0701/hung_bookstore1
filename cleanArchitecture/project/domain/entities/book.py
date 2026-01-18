"""
Book Entity - Core business object
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal


@dataclass
class Book:
    """Book entity representing a book in the catalog"""
    id: Optional[int] = None
    title: str = ""
    author: str = ""
    price: Decimal = Decimal("0.00")
    stock: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_available(self) -> bool:
        """Check if book is in stock"""
        return self.stock > 0

    def can_purchase(self, quantity: int) -> bool:
        """Check if requested quantity is available"""
        return self.stock >= quantity

    def to_dict(self) -> dict:
        """Convert entity to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'price': float(self.price),
            'stock': self.stock,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
