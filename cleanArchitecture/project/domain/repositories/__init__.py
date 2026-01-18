# Repository Interfaces (Abstract classes)
from .customer_repository import CustomerRepositoryInterface
from .book_repository import BookRepositoryInterface
from .cart_repository import CartRepositoryInterface

__all__ = ['CustomerRepositoryInterface', 'BookRepositoryInterface', 'CartRepositoryInterface']
