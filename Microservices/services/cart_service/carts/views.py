"""
Cart Service API Views
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, AddToCartSerializer
from .service_client import ServiceClient


@api_view(['GET'])
def get_cart(request, customer_id):
    """
    API endpoint to get customer's cart
    GET /api/cart/<customer_id>/
    """
    # Verify customer exists via Customer Service
    if not ServiceClient.check_customer_exists(customer_id):
        return Response({
            'success': False,
            'message': 'Không tìm thấy khách hàng!'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Get or create cart
    cart, created = Cart.objects.get_or_create(customer_id=customer_id)
    
    # Get cart items with book details
    cart_items = []
    total = 0
    
    for item in cart.items.all():
        book_data = ServiceClient.get_book(item.book_id)
        if book_data:
            item_total = float(book_data['price']) * item.quantity
            cart_items.append({
                'id': item.id,
                'book_id': item.book_id,
                'book_title': book_data['title'],
                'book_author': book_data['author'],
                'book_price': book_data['price'],
                'quantity': item.quantity,
                'item_total': item_total
            })
            total += item_total
    
    return Response({
        'success': True,
        'cart': {
            'id': cart.id,
            'customer_id': customer_id,
            'items': cart_items,
            'total': total,
            'item_count': len(cart_items)
        }
    })


@api_view(['POST'])
def add_to_cart(request):
    """
    API endpoint to add book to cart
    POST /api/cart/add/
    Body: {"customer_id": 1, "book_id": 1, "quantity": 1}
    """
    serializer = AddToCartSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    customer_id = serializer.validated_data['customer_id']
    book_id = serializer.validated_data['book_id']
    quantity = serializer.validated_data['quantity']
    
    # Verify customer exists
    if not ServiceClient.check_customer_exists(customer_id):
        return Response({
            'success': False,
            'message': 'Không tìm thấy khách hàng!'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Verify book exists and has stock
    stock_info = ServiceClient.check_book_stock(book_id)
    if not stock_info:
        return Response({
            'success': False,
            'message': 'Không tìm thấy sách!'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if not stock_info.get('available', False):
        return Response({
            'success': False,
            'message': 'Sách đã hết hàng!'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if stock_info.get('stock', 0) < quantity:
        return Response({
            'success': False,
            'message': f'Chỉ còn {stock_info["stock"]} sách trong kho!'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Get or create cart
    cart, _ = Cart.objects.get_or_create(customer_id=customer_id)
    
    # Check if item already in cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book_id=book_id,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    # Update book stock
    ServiceClient.update_book_stock(book_id, -quantity)
    
    return Response({
        'success': True,
        'message': 'Đã thêm sách vào giỏ hàng!',
        'cart_item': {
            'id': cart_item.id,
            'book_id': book_id,
            'quantity': cart_item.quantity
        }
    }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@api_view(['DELETE'])
def remove_from_cart(request, customer_id, item_id):
    """
    API endpoint to remove item from cart
    DELETE /api/cart/<customer_id>/remove/<item_id>/
    """
    try:
        cart = Cart.objects.get(customer_id=customer_id)
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
        
        # Restore book stock
        ServiceClient.update_book_stock(cart_item.book_id, cart_item.quantity)
        
        cart_item.delete()
        
        return Response({
            'success': True,
            'message': 'Đã xóa sách khỏi giỏ hàng!'
        })
    except Cart.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Không tìm thấy giỏ hàng!'
        }, status=status.HTTP_404_NOT_FOUND)
    except CartItem.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Không tìm thấy sản phẩm trong giỏ hàng!'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def clear_cart(request, customer_id):
    """
    API endpoint to clear cart
    DELETE /api/cart/<customer_id>/clear/
    """
    try:
        cart = Cart.objects.get(customer_id=customer_id)
        
        # Restore stock for all items
        for item in cart.items.all():
            ServiceClient.update_book_stock(item.book_id, item.quantity)
        
        cart.items.all().delete()
        
        return Response({
            'success': True,
            'message': 'Đã xóa toàn bộ giỏ hàng!'
        })
    except Cart.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Không tìm thấy giỏ hàng!'
        }, status=status.HTTP_404_NOT_FOUND)
