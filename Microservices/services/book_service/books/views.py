"""
Book Service API Views
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg

from .models import Book
from .serializers import BookSerializer, StaffLoginSerializer


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
            'stock_quantity': book.stock_quantity,
            'available': book.stock_quantity > 0
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
        
        book.stock_quantity += quantity_change
        if book.stock_quantity < 0:
            book.stock_quantity = 0
        book.save()
        
        return Response({
            'success': True,
            'book_id': book.id,
            'new_stock': book.stock_quantity
        })
    except Book.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Không tìm thấy sách!'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def add_book(request):
    """
    API endpoint to add a new book (staff only)
    POST /api/books/
    Body: {"title": "...", "author": "...", "price": 10.99, "stock_quantity": 100}
    """
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        book = serializer.save()
        return Response({
            'success': True,
            'book': BookSerializer(book).data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_recommendations(request):
    """
    API endpoint to get book recommendations
    GET /api/books/recommendations/?customer_id=1
    """
    customer_id = request.query_params.get('customer_id')
    if customer_id:
        books = Book.recommend_for_customer(customer_id)
    else:
        # Default: top rated
        books = Book.objects.annotate(avg_rating=Avg('ratings__score')).order_by('-avg_rating')[:5]
    return Response({
        'success': True,
        'books': BookSerializer(books, many=True).data
    })


@api_view(['POST'])
def staff_login(request):
    """
    API endpoint for staff login
    POST /api/staff/login/
    """
    serializer = StaffLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Simple check: assume staff email is 'staff@bookstore.com', password 'staff'
        if email == 'staff@bookstore.com' and password == 'staff':
            return Response({
                'success': True,
                'message': 'Đăng nhập staff thành công!',
                'staff': {'email': email}
            })
        else:
            return Response({
                'success': False,
                'message': 'Thông tin đăng nhập không đúng!'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
