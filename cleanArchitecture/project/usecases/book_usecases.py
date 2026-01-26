"""
Book Use Cases - Application Business Rules
"""
from typing import List, Optional

from ..domain.entities.book import Book
from ..domain.repositories.book_repository import BookRepositoryInterface


class GetBookCatalogUseCase:
    """Use case for getting book catalog"""

    def __init__(self, book_repository: BookRepositoryInterface):
        self.book_repository = book_repository

    def execute(self, search_query: str = "") -> List[Book]:
        """
        Get all books, optionally filtered by search query
        
        Args:
            search_query: Optional search term for title/author
            
        Returns:
            List of Book entities
        """
        if search_query:
            return self.book_repository.search(search_query)
        return self.book_repository.get_all()


class GetBookDetailUseCase:
    """Use case for getting book details"""

    def __init__(self, book_repository: BookRepositoryInterface):
        self.book_repository = book_repository

    def execute(self, book_id: int) -> Optional[Book]:
        """
        Get book details by ID
        
        Args:
            book_id: Book's ID
            
        Returns:
            Book entity or None
        """
        return self.book_repository.get_by_id(book_id)


class AddBookUseCase:
    """Use case for adding a new book"""

    def __init__(self, book_repository: BookRepositoryInterface):
        self.book_repository = book_repository

    def execute(self, title: str, author: str, price: float, stock_quantity: int) -> Book:
        """
        Add a new book
        
        Args:
            title: Book title
            author: Book author
            price: Book price
            stock_quantity: Initial stock
            
        Returns:
            Created Book entity
        """
        return self.book_repository.create(title, author, price, stock_quantity)


class GetBookRecommendationsUseCase:
    """Use case for getting book recommendations"""

    def __init__(self, book_repository: BookRepositoryInterface):
        self.book_repository = book_repository

    def execute(self, customer_id: int, limit: int = 5) -> List[Book]:
        """
        Get book recommendations for customer
        
        Args:
            customer_id: Customer ID
            limit: Max number of recommendations
            
        Returns:
            List of recommended Book entities
        """
        # For simplicity, return top books by stock
        return self.book_repository.get_all()[:limit]
