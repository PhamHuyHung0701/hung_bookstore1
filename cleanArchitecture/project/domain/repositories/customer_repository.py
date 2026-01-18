"""
Customer Repository Interface - Abstract base class
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.customer import Customer


class CustomerRepositoryInterface(ABC):
    """Interface for Customer repository"""

    @abstractmethod
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """Get customer by ID"""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email"""
        pass

    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        """Create a new customer"""
        pass

    @abstractmethod
    def update(self, customer: Customer) -> Customer:
        """Update an existing customer"""
        pass

    @abstractmethod
    def delete(self, customer_id: int) -> bool:
        """Delete a customer"""
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """Check if email already exists"""
        pass
