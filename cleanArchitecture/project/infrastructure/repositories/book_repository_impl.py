"""
Book Repository Implementation - Django ORM
"""
from typing import Optional, List
from decimal import Decimal
from django.db.models import Q

from ...domain.entities.book import Book
from ...domain.repositories.book_repository import BookRepositoryInterface
from ..orm.models import BookModel


class DjangoBookRepository(BookRepositoryInterface):
    """Django ORM implementation of Book Repository"""

    def _to_entity(self, model: BookModel) -> Book:
        """Convert ORM model to domain entity"""
        return Book(
            id=model.id,
            title=model.title,
            author=model.author,
            price=Decimal(str(model.price)),
            stock=model.stock,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def get_all(self) -> List[Book]:
        """Get all books"""
        models = BookModel.objects.all()
        return [self._to_entity(m) for m in models]

    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Get book by ID"""
        try:
            model = BookModel.objects.get(id=book_id)
            return self._to_entity(model)
        except BookModel.DoesNotExist:
            return None

    def search(self, query: str) -> List[Book]:
        """Search books by title or author"""
        models = BookModel.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
        return [self._to_entity(m) for m in models]

    def update_stock(self, book_id: int, quantity: int) -> bool:
        """Update book stock"""
        try:
            model = BookModel.objects.get(id=book_id)
            model.stock = quantity
            model.save()
            return True
        except BookModel.DoesNotExist:
            return False
