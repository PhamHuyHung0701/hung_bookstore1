"""
Cart Service API Views
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Cart, CartItem, Order, OrderItem, Shipping, Payment
from .serializers import CartSerializer, CartItemSerializer, AddToCartSerializer, CheckoutSerializer, OrderSerializer, ShippingSerializer, PaymentSerializer
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
    
    if stock_info.get('stock_quantity', 0) < quantity:
        return Response({
            'success': False,
            'message': f'Chỉ còn {stock_info["stock_quantity"]} sách trong kho!'
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


@api_view(['PUT'])
def update_cart_item(request, customer_id, item_id):
    """
    API endpoint to update cart item quantity
    PUT /api/cart/<customer_id>/update/<item_id>/
    Body: {"quantity": 2}
    """
    try:
        cart = Cart.objects.get(customer_id=customer_id)
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
        
        new_quantity = request.data.get('quantity', cart_item.quantity)
        if new_quantity <= 0:
            # Remove item
            ServiceClient.update_book_stock(cart_item.book_id, cart_item.quantity)
            cart_item.delete()
            return Response({
                'success': True,
                'message': 'Đã xóa sản phẩm khỏi giỏ hàng!'
            })
        
        quantity_diff = new_quantity - cart_item.quantity
        
        # Check stock
        stock_info = ServiceClient.check_book_stock(cart_item.book_id)
        if not stock_info or stock_info.get('stock_quantity', 0) < quantity_diff:
            return Response({
                'success': False,
                'message': 'Không đủ hàng trong kho!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update stock
        ServiceClient.update_book_stock(cart_item.book_id, -quantity_diff)
        
        cart_item.quantity = new_quantity
        cart_item.save()
        
        return Response({
            'success': True,
            'cart_item': {
                'id': cart_item.id,
                'book_id': cart_item.book_id,
                'quantity': cart_item.quantity
            }
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


@api_view(['POST'])
def checkout(request):
    """
    API endpoint to checkout cart
    POST /api/cart/checkout/
    Body: {"customer_id": 1, "shipping_id": 1, "payment_id": 1}
    """
    serializer = CheckoutSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    customer_id = serializer.validated_data['customer_id']
    shipping_id = serializer.validated_data['shipping_id']
    payment_id = serializer.validated_data['payment_id']
    
    try:
        cart = Cart.objects.get(customer_id=customer_id, is_active=True)
    except Cart.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Không tìm thấy giỏ hàng!'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if not cart.items.exists():
        return Response({
            'success': False,
            'message': 'Giỏ hàng trống!'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Calculate total
    total = 0
    for item in cart.items.all():
        book_data = ServiceClient.get_book(item.book_id)
        if book_data:
            total += float(book_data['price']) * item.quantity
    
    # Get shipping fee
    try:
        shipping = Shipping.objects.get(id=shipping_id)
        total += float(shipping.fee)
    except Shipping.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Phương thức vận chuyển không hợp lệ!'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Create order
    order = Order.objects.create(customer_id=customer_id, total_price=total)
    
    # Create order items
    for item in cart.items.all():
        OrderItem.objects.create(order=order, book_id=item.book_id, quantity=item.quantity)
    
    # Deactivate cart
    cart.is_active = False
    cart.save()
    
    # Update payment status? For simplicity, assume success
    try:
        payment = Payment.objects.get(id=payment_id)
        payment.status = 'completed'
        payment.save()
    except Payment.DoesNotExist:
        pass  # Ignore for now
    
    return Response({
        'success': True,
        'order': OrderSerializer(order).data
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_order_history(request, customer_id):
    """
    API endpoint to get customer's order history
    GET /api/cart/<customer_id>/orders/
    """
    orders = Order.objects.filter(customer_id=customer_id).order_by('-created_at')
    order_data = []
    
    for order in orders:
        items = []
        for item in order.items.all():
            book_data = ServiceClient.get_book(item.book_id)
            if book_data:
                items.append({
                    'book_id': item.book_id,
                    'book_title': book_data['title'],
                    'quantity': item.quantity,
                    'price': book_data['price']
                })
        order_data.append({
            'id': order.id,
            'total_price': order.total_price,
            'created_at': order.created_at,
            'items': items
        })
    
    return Response({
        'success': True,
        'orders': order_data
    })


@api_view(['GET'])
def get_shipping_options(request):
    """
    API endpoint to get shipping options
    GET /api/cart/shipping/
    """
    shipping = Shipping.objects.all()
    return Response({
        'success': True,
        'shipping_options': ShippingSerializer(shipping, many=True).data
    })


@api_view(['GET'])
def get_payment_options(request):
    """
    API endpoint to get payment options
    GET /api/cart/payment/
    """
    payments = Payment.objects.all()
    return Response({
        'success': True,
        'payment_options': PaymentSerializer(payments, many=True).data
    })
