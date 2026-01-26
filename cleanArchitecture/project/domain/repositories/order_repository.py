"""
Order Repository Interface - Abstract base class
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.order import Order


class OrderRepositoryInterface(ABC):
    """Interface for Order repository"""

    @abstractmethod
    def create(self, customer_id: int, total_price: float, shipping_id: int, payment_id: int) -> Order:
        """Create a new order"""
        pass

    @abstractmethod
    def get_by_customer_id(self, customer_id: int) -> List[Order]:
        """Get orders by customer ID"""
        pass

    @abstractmethod
    def add_item(self, order_id: int, book_id: int, quantity: int, price: float) -> None:
        """Add item to order"""
        pass
