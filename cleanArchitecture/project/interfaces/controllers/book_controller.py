"""
Book Controller - Interface Adapter Layer
Handles HTTP request/response and coordinates with Use Cases
"""
from typing import Dict, Any, List

from ...usecases.book_usecases import (
    GetBookCatalogUseCase,
    GetBookDetailUseCase
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
