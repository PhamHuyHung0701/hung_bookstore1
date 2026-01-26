"""
Shipping and Payment Repository Interface - Abstract base class
"""
from abc import ABC, abstractmethod
from typing import List
from ..entities.shipping_payment import Shipping, Payment


class ShippingPaymentRepositoryInterface(ABC):
    """Interface for Shipping and Payment repository"""

    @abstractmethod
    def get_all_shippings(self) -> List[Shipping]:
        """Get all shipping options"""
        pass

    @abstractmethod
    def get_all_payments(self) -> List[Payment]:
        """Get all payment options"""
        pass
