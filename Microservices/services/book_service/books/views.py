"""
Book Service API Views
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer


@api_view(['GET'])
def list_books(request):
    """
    API endpoint to list all books
    GET /api/books/
    """
    books = Book.objects.all()
    return Response({
        'success': True,
        'books': BookSerializer(books, many=True).data
    })


@api_view(['GET'])
def get_book(request, book_id):
    """
    API endpoint to get book by ID
    GET /api/books/<book_id>/
    """
    try:
        book = Book.objects.get(id=book_id)
        return Response({
            'success': True,
            'book': BookSerializer(book).data
        })
    except Book.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Không tìm thấy sách!'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def check_stock(request, book_id):
    """
    API endpoint to check book stock
    GET /api/books/<book_id>/stock/
    """
    try:
        book = Book.objects.get(id=book_id)
        return Response({
            'book_id': book.id,
            'title': book.title,
            'stock': book.stock,
            'available': book.stock > 0
        })
    except Book.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Không tìm thấy sách!'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_stock(request, book_id):
    """
    API endpoint to update book stock
    POST /api/books/<book_id>/stock/
    Body: {"quantity_change": -1} (negative to decrease, positive to increase)
    """
    try:
        book = Book.objects.get(id=book_id)
        quantity_change = request.data.get('quantity_change', 0)
        
        book.stock += quantity_change
        if book.stock < 0:
            book.stock = 0
        book.save()
        
        return Response({
            'success': True,
            'book_id': book.id,
            'new_stock': book.stock
        })
    except Book.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Không tìm thấy sách!'
        }, status=status.HTTP_404_NOT_FOUND)
