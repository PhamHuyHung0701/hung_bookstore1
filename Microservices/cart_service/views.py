"""
Cart Service API Views
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import (
    CartSerializer, 
    CartItemSerializer, 
    AddToCartSerializer,
    UpdateCartItemSerializer
)
from .service_client import ServiceClient


@api_view(['GET'])
def get_cart(request, customer_id):
    """
    API endpoint to get customer's cart
    GET /api/cart/<customer_id>/
    """
    # Verify customer exists via customer_service
    if not ServiceClient.check_customer_exists(customer_id):
        return Response({
            'success': False,
            'message': 'Không tìm thấy khách hàng!'
        }, status=status.HTTP_404_NOT_FOUND)

    # Get or create cart
    cart, created = Cart.objects.get_or_create(customer_id=customer_id)
    
    return Response({
        'success': True,
        'cart': CartSerializer(cart).data
    })


@api_view(['POST'])
def add_to_cart(request, customer_id):
    """
    API endpoint to add book to cart
    POST /api/cart/<customer_id>/add/
    """
    # Verify customer exists
    if not ServiceClient.check_customer_exists(customer_id):
        return Response({
            'success': False,
            'message': 'Không tìm thấy khách hàng!'
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = AddToCartSerializer(data=request.data)
    
    if serializer.is_valid():
        book_id = serializer.validated_data['book_id']
        quantity = serializer.validated_data['quantity']

        # Check book stock from book_service
        book_stock = ServiceClient.check_book_stock(book_id)
        if not book_stock:
            return Response({
                'success': False,
                'message': 'Không tìm thấy sách!'
            }, status=status.HTTP_404_NOT_FOUND)

        if not book_stock.get('available'):
            return Response({
                'success': False,
                'message': 'Sách đã hết hàng!'
            }, status=status.HTTP_400_BAD_REQUEST)

        if book_stock.get('stock', 0) < quantity:
            return Response({
                'success': False,
                'message': 'Không đủ số lượng trong kho!'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get or create cart
        cart, _ = Cart.objects.get_or_create(customer_id=customer_id)

        # Check if item already exists
        try:
            cart_item = CartItem.objects.get(cart=cart, book_id=book_id)
            new_quantity = cart_item.quantity + quantity
            if new_quantity <= book_stock.get('stock', 0):
                cart_item.quantity = new_quantity
                cart_item.save()
            else:
                return Response({
                    'success': False,
                    'message': 'Không thể thêm nhiều hơn số lượng trong kho!'
                }, status=status.HTTP_400_BAD_REQUEST)
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                cart=cart,
                book_id=book_id,
                quantity=quantity
            )

        return Response({
            'success': True,
            'message': f'Đã thêm "{book_stock.get("title")}" vào giỏ hàng!',
            'cart_item': CartItemSerializer(cart_item).data
        }, status=status.HTTP_201_CREATED)

    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_cart_item(request, customer_id, item_id):
    """
    API endpoint to update cart item quantity
    PUT /api/cart/<customer_id>/items/<item_id>/
    """
    try:
        cart = Cart.objects.get(customer_id=customer_id)
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
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

    serializer = UpdateCartItemSerializer(data=request.data)
    
    if serializer.is_valid():
        quantity = serializer.validated_data['quantity']

        if quantity <= 0:
            # Remove item
            cart_item.delete()
            return Response({
                'success': True,
                'message': 'Đã xóa sách khỏi giỏ hàng!'
            })

        # Check book stock
        book_stock = ServiceClient.check_book_stock(cart_item.book_id)
        if book_stock and quantity > book_stock.get('stock', 0):
            return Response({
                'success': False,
                'message': 'Số lượng không hợp lệ!'
            }, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = quantity
        cart_item.save()

        return Response({
            'success': True,
            'message': 'Đã cập nhật số lượng!',
            'cart_item': CartItemSerializer(cart_item).data
        })

    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def remove_from_cart(request, customer_id, item_id):
    """
    API endpoint to remove item from cart
    DELETE /api/cart/<customer_id>/items/<item_id>/
    """
    try:
        cart = Cart.objects.get(customer_id=customer_id)
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
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

    cart_item.delete()

    return Response({
        'success': True,
        'message': 'Đã xóa sách khỏi giỏ hàng!'
    })


@api_view(['DELETE'])
def clear_cart(request, customer_id):
    """
    API endpoint to clear all items from cart
    DELETE /api/cart/<customer_id>/clear/
    """
    try:
        cart = Cart.objects.get(customer_id=customer_id)
        cart.items.all().delete()
        return Response({
            'success': True,
            'message': 'Đã xóa tất cả sản phẩm khỏi giỏ hàng!'
        })
    except Cart.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Không tìm thấy giỏ hàng!'
        }, status=status.HTTP_404_NOT_FOUND)
