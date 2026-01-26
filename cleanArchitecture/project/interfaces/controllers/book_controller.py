"""
Book Controller - Interface Adapter Layer
Handles HTTP request/response and coordinates with Use Cases
"""
from typing import Dict, Any, List

from ...usecases.book_usecases import (
    GetBookCatalogUseCase,
    GetBookDetailUseCase,
    AddBookUseCase,
    GetBookRecommendationsUseCase
)
from ...infrastructure.repositories.book_repository_impl import DjangoBookRepository


class BookController:
    """Controller for book-related operations"""

    def __init__(self):
        self.book_repository = DjangoBookRepository()

    def get_catalog(self, search_query: str = "") -> Dict[str, Any]:
        """
        Get book catalog
        
        Returns:
            Dict with 'success', 'books', and 'search_query'
        """
        use_case = GetBookCatalogUseCase(self.book_repository)
        books = use_case.execute(search_query)
        
        return {
            'success': True,
            'books': books,
            'search_query': search_query
        }

    def get_detail(self, book_id: int) -> Dict[str, Any]:
        """
        Get book details
        
        Returns:
            Dict with 'success' and optionally 'book'
        """
        use_case = GetBookDetailUseCase(self.book_repository)
        book = use_case.execute(book_id)

        if book:
            return {
                'success': True,
                'book': book
            }
        return {
            'success': False,
            'message': 'Không tìm thấy sách'
        }

    def add_book(self, title: str, author: str, price: str, stock_quantity: str) -> Dict[str, Any]:
        """
        Add a new book
        
        Returns:
            Dict with 'success' and optionally 'message'
        """
        try:
            price_decimal = float(price)
            stock = int(stock_quantity)
            use_case = AddBookUseCase(self.book_repository)
            book = use_case.execute(title, author, price_decimal, stock)
            return {
                'success': True,
                'book': book
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }

    def get_recommendations(self, customer_id: int) -> Dict[str, Any]:
        """
        Get book recommendations for customer
        
        Returns:
            Dict with 'success' and 'books'
        """
        use_case = GetBookRecommendationsUseCase(self.book_repository)
        books = use_case.execute(customer_id)
        return {
            'success': True,
            'books': books
        }
