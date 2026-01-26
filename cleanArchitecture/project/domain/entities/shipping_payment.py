"""
Shipping and Payment Entities - Core business objects
"""
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass
class Shipping:
    """Shipping entity representing a shipping method"""
    id: Optional[int] = None
    method_name: str = ""
    fee: Decimal = Decimal("0.00")

    def to_dict(self) -> dict:
        """Convert entity to dictionary"""
        return {
            'id': self.id,
            'method_name': self.method_name,
            'fee': float(self.fee)
        }


@dataclass
class Payment:
    """Payment entity representing a payment method"""
    id: Optional[int] = None
    method_name: str = ""
    status: str = "pending"

    def to_dict(self) -> dict:
        """Convert entity to dictionary"""
        return {
            'id': self.id,
            'method_name': self.method_name,
            'status': self.status
        }
