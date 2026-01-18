"""
Cart Repository Interface - Abstract base class
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.cart import Cart, CartItem


class CartRepositoryInterface(ABC):
    """Interface for Cart repository"""

    @abstractmethod
    def get_by_customer_id(self, customer_id: int) -> Optional[Cart]:
        """Get cart by customer ID"""
        pass

    @abstractmethod
    def get_or_create(self, customer_id: int) -> Cart:
        """Get existing cart or create new one for customer"""
        pass

    @abstractmethod
    def add_item(self, cart_id: int, book_id: int, quantity: int) -> CartItem:
        """Add item to cart"""
        pass

    @abstractmethod
    def update_item_quantity(self, item_id: int, quantity: int) -> Optional[CartItem]:
        """Update cart item quantity"""
        pass

    @abstractmethod
    def remove_item(self, item_id: int) -> bool:
        """Remove item from cart"""
        pass

    @abstractmethod
    def get_cart_item(self, item_id: int) -> Optional[CartItem]:
        """Get cart item by ID"""
        pass

    @abstractmethod
    def get_cart_items(self, cart_id: int) -> List[CartItem]:
        """Get all items in a cart"""
        pass
