"""
Cart Controller - Interface Adapter Layer
Handles HTTP request/response and coordinates with Use Cases
"""
from typing import Dict, Any

from ...usecases.cart_usecases import (
    GetCartUseCase,
    AddToCartUseCase,
    UpdateCartItemUseCase,
    RemoveFromCartUseCase,
    CheckoutUseCase,
    GetOrderHistoryUseCase,
    GetShippingOptionsUseCase,
    GetPaymentOptionsUseCase
)
from ...infrastructure.repositories.cart_repository_impl import DjangoCartRepository
from ...infrastructure.repositories.book_repository_impl import DjangoBookRepository
from ...infrastructure.repositories.order_repository_impl import DjangoOrderRepository
from ...infrastructure.repositories.shipping_payment_repository_impl import DjangoShippingPaymentRepository


class CartController:
    """Controller for cart-related operations"""

    def __init__(self):
        self.cart_repository = DjangoCartRepository()
        self.book_repository = DjangoBookRepository()
        self.order_repository = DjangoOrderRepository()
        self.shipping_payment_repository = DjangoShippingPaymentRepository()

    def get_cart(self, customer_id: int) -> Dict[str, Any]:
        """
        Get customer's cart
        
        Returns:
            Dict with 'success', 'cart', and 'cart_items'
        """
        use_case = GetCartUseCase(self.cart_repository)
        cart = use_case.execute(customer_id)
        
        return {
            'success': True,
            'cart': cart,
            'cart_items': cart.items if cart else []
        }

    def add_to_cart(self, customer_id: int, book_id: int, 
                    quantity: int = 1) -> Dict[str, Any]:
        """
        Add book to cart
        
        Returns:
            Dict with 'success', 'message', and optionally 'cart_item'
        """
        try:
            use_case = AddToCartUseCase(self.cart_repository, self.book_repository)
            cart_item = use_case.execute(customer_id, book_id, quantity)
            
            # Get book title for message
            book = self.book_repository.get_by_id(book_id)
            book_title = book.title if book else "Sách"
            
            return {
                'success': True,
                'message': f'Đã thêm "{book_title}" vào giỏ hàng!',
                'cart_item': cart_item
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }

    def update_cart_item(self, customer_id: int, item_id: int, 
                         quantity: int) -> Dict[str, Any]:
        """
        Update cart item quantity
        
        Returns:
            Dict with 'success' and 'message'
        """
        try:
            use_case = UpdateCartItemUseCase(self.cart_repository, self.book_repository)
            result = use_case.execute(customer_id, item_id, quantity)
            
            if result is None:
                return {
                    'success': True,
                    'message': 'Đã xóa sách khỏi giỏ hàng!'
                }
            return {
                'success': True,
                'message': 'Đã cập nhật số lượng!'
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }

    def remove_from_cart(self, customer_id: int, item_id: int) -> Dict[str, Any]:
        """
        Remove item from cart
        
        Returns:
            Dict with 'success' and 'message'
        """
        try:
            use_case = RemoveFromCartUseCase(self.cart_repository)
            use_case.execute(customer_id, item_id)
            
            return {
                'success': True,
                'message': 'Đã xóa sách khỏi giỏ hàng!'
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }

    def checkout(self, customer_id: int, shipping_id: str, payment_id: str) -> Dict[str, Any]:
        """
        Checkout cart
        
        Returns:
            Dict with 'success' and 'message'
        """
        try:
            use_case = CheckoutUseCase(self.cart_repository, self.book_repository, self.order_repository)
            order = use_case.execute(customer_id, int(shipping_id), int(payment_id))
            
            return {
                'success': True,
                'message': f'Đặt hàng thành công! Mã đơn: {order.id}'
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }

    def get_order_history(self, customer_id: int) -> Dict[str, Any]:
        """
        Get order history
        
        Returns:
            Dict with 'success' and 'orders'
        """
        use_case = GetOrderHistoryUseCase(self.order_repository)
        orders = use_case.execute(customer_id)
        
        return {
            'success': True,
            'orders': orders
        }

    def get_shipping_options(self) -> Dict[str, Any]:
        """
        Get shipping options
        
        Returns:
            Dict with 'success' and 'shippings'
        """
        use_case = GetShippingOptionsUseCase(self.shipping_payment_repository)
        shippings = use_case.execute()
        
        return {
            'success': True,
            'shippings': shippings
        }

    def get_payment_options(self) -> Dict[str, Any]:
        """
        Get payment options
        
        Returns:
            Dict with 'success' and 'payments'
        """
        use_case = GetPaymentOptionsUseCase(self.shipping_payment_repository)
        payments = use_case.execute()
        
        return {
            'success': True,
            'payments': payments
        }
