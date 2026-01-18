"""
Book Repository Interface - Abstract base class
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.book import Book


class BookRepositoryInterface(ABC):
    """Interface for Book repository"""

    @abstractmethod
    def get_all(self) -> List[Book]:
        """Get all books"""
        pass

    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Get book by ID"""
        pass

    @abstractmethod
    def search(self, query: str) -> List[Book]:
        """Search books by title or author"""
        pass

    @abstractmethod
    def update_stock(self, book_id: int, quantity: int) -> bool:
        """Update book stock"""
        pass
