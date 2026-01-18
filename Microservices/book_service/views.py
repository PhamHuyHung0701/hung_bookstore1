"""
Book Service API Views
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

from .models import Book
from .serializers import BookSerializer, BookStockUpdateSerializer


@api_view(['GET'])
def list_books(request):
    """
    API endpoint to list all books with optional search
    GET /api/books/
    GET /api/books/?search=keyword
    """
    search_query = request.GET.get('search', '')
    
    if search_query:
        books = Book.objects.filter(
            Q(title__icontains=search_query) | Q(author__icontains=search_query)
        )
    else:
        books = Book.objects.all()
    
    return Response({
        'success': True,
        'books': BookSerializer(books, many=True).data,
        'search_query': search_query
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
def check_book_stock(request, book_id):
    """
    API endpoint to check book stock (used by cart_service)
    GET /api/books/<book_id>/stock/
    """
    try:
        book = Book.objects.get(id=book_id)
        return Response({
            'success': True,
            'book_id': book.id,
            'title': book.title,
            'price': float(book.price),
            'stock': book.stock,
            'available': book.is_available()
        })
    except Book.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Không tìm thấy sách!'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_stock(request, book_id):
    """
    API endpoint to update book stock (used by cart_service for checkout)
    PUT /api/books/<book_id>/stock/
    """
    try:
        book = Book.objects.get(id=book_id)
        serializer = BookStockUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            quantity = serializer.validated_data['quantity']
            if book.stock + quantity < 0:
                return Response({
                    'success': False,
                    'message': 'Không đủ số lượng trong kho!'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            book.stock += quantity
            book.save()
            
            return Response({
                'success': True,
                'message': 'Đã cập nhật số lượng!',
                'book': BookSerializer(book).data
            })
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Book.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Không tìm thấy sách!'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def check_book_exists(request, book_id):
    """
    API endpoint to check if book exists (used by other services)
    GET /api/books/<book_id>/exists/
    """
    exists = Book.objects.filter(id=book_id).exists()
    return Response({
        'exists': exists
    })
