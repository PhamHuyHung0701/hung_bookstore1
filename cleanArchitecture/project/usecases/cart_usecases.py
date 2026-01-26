"""
Cart Use Cases - Application Business Rules
"""
from typing import Optional, List

from ..domain.entities.cart import Cart, CartItem
from ..domain.entities.order import Order
from ..domain.entities.shipping_payment import Shipping, Payment
from ..domain.repositories.cart_repository import CartRepositoryInterface
from ..domain.repositories.book_repository import BookRepositoryInterface
from ..domain.repositories.order_repository import OrderRepositoryInterface
from ..domain.repositories.shipping_payment_repository import ShippingPaymentRepositoryInterface


class GetCartUseCase:
    """Use case for getting customer's cart"""

    def __init__(self, cart_repository: CartRepositoryInterface):
        self.cart_repository = cart_repository

    def execute(self, customer_id: int) -> Cart:
        """
        Get or create cart for customer
        
        Args:
            customer_id: Customer's ID
            
        Returns:
            Cart entity with items
        """
        return self.cart_repository.get_or_create(customer_id)


class AddToCartUseCase:
    """Use case for adding book to cart"""

    def __init__(self, cart_repository: CartRepositoryInterface, 
                 book_repository: BookRepositoryInterface):
        self.cart_repository = cart_repository
        self.book_repository = book_repository

    def execute(self, customer_id: int, book_id: int, quantity: int = 1) -> CartItem:
        """
        Add book to customer's cart
        
        Args:
            customer_id: Customer's ID
            book_id: Book's ID
            quantity: Quantity to add
            
        Returns:
            Created/updated CartItem entity
            
        Raises:
            ValueError: If book not found or out of stock
        """
        # Get book
        book = self.book_repository.get_by_id(book_id)
        if not book:
            raise ValueError("Sách không tồn tại!")

        if not book.is_available():
            raise ValueError("Sách đã hết hàng!")

        if not book.can_purchase(quantity):
            raise ValueError("Không đủ số lượng trong kho!")

        # Get or create cart
        cart = self.cart_repository.get_or_create(customer_id)

        # Add item to cart
        return self.cart_repository.add_item(cart.id, book_id, quantity)


class UpdateCartItemUseCase:
    """Use case for updating cart item quantity"""

    def __init__(self, cart_repository: CartRepositoryInterface,
                 book_repository: BookRepositoryInterface):
        self.cart_repository = cart_repository
        self.book_repository = book_repository

    def execute(self, customer_id: int, item_id: int, quantity: int) -> Optional[CartItem]:
        """
        Update cart item quantity
        
        Args:
            customer_id: Customer's ID (for verification)
            item_id: CartItem's ID
            quantity: New quantity
            
        Returns:
            Updated CartItem entity or None if deleted
            
        Raises:
            ValueError: If validation fails
        """
        # Get cart item
        cart_item = self.cart_repository.get_cart_item(item_id)
        if not cart_item:
            raise ValueError("Không tìm thấy sản phẩm trong giỏ hàng!")

        # Get cart to verify ownership
        cart = self.cart_repository.get_by_customer_id(customer_id)
        if not cart or cart.id != cart_item.cart_id:
            raise ValueError("Bạn không có quyền thực hiện thao tác này!")

        if quantity <= 0:
            # Remove item
            self.cart_repository.remove_item(item_id)
            return None

        # Validate stock
        book = self.book_repository.get_by_id(cart_item.book_id)
        if book and quantity > book.stock:
            raise ValueError("Số lượng không hợp lệ!")

        return self.cart_repository.update_item_quantity(item_id, quantity)


class RemoveFromCartUseCase:
    """Use case for removing item from cart"""

    def __init__(self, cart_repository: CartRepositoryInterface):
        self.cart_repository = cart_repository

    def execute(self, customer_id: int, item_id: int) -> bool:
        """
        Remove item from cart
        
        Args:
            customer_id: Customer's ID (for verification)
            item_id: CartItem's ID
            
        Returns:
            True if removed successfully
            
        Raises:
            ValueError: If validation fails
        """
        # Get cart item
        cart_item = self.cart_repository.get_cart_item(item_id)
        if not cart_item:
            raise ValueError("Không tìm thấy sản phẩm trong giỏ hàng!")

        # Verify ownership
        cart = self.cart_repository.get_by_customer_id(customer_id)
        if not cart or cart.id != cart_item.cart_id:
            raise ValueError("Bạn không có quyền thực hiện thao tác này!")

        return self.cart_repository.remove_item(item_id)


class CheckoutUseCase:
    """Use case for checking out cart"""

    def __init__(self, cart_repository: CartRepositoryInterface,
                 book_repository: BookRepositoryInterface,
                 order_repository: OrderRepositoryInterface):
        self.cart_repository = cart_repository
        self.book_repository = book_repository
        self.order_repository = order_repository

    def execute(self, customer_id: int, shipping_id: int, payment_id: int) -> Order:
        """
        Checkout cart and create order
        
        Args:
            customer_id: Customer's ID
            shipping_id: Shipping method ID
            payment_id: Payment method ID
            
        Returns:
            Created Order entity
            
        Raises:
            ValueError: If cart is empty or validation fails
        """
        # Get cart
        cart = self.cart_repository.get_by_customer_id(customer_id)
        if not cart or not cart.items:
            raise ValueError("Giỏ hàng trống!")

        # Calculate total (simplified, no shipping fee)
        total = cart.get_total()

        # Create order
        order = self.order_repository.create(customer_id, float(total), shipping_id, payment_id)

        # Add items to order and update stock
        for item in cart.items:
            self.order_repository.add_item(order.id, item.book_id, item.quantity, float(item.book.price))
            # Update stock
            self.book_repository.update_stock(item.book_id, item.book.stock_quantity - item.quantity)

        # Clear cart
        for item in cart.items:
            self.cart_repository.remove_item(item.id)
        
        # Deactivate cart
        cart.is_active = False
        # Assume repository has update method, but for simplicity, skip

        return order


class GetOrderHistoryUseCase:
    """Use case for getting order history"""

    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    def execute(self, customer_id: int) -> List[Order]:
        """
        Get order history for customer
        
        Args:
            customer_id: Customer's ID
            
        Returns:
            List of Order entities
        """
        return self.order_repository.get_by_customer_id(customer_id)


class GetShippingOptionsUseCase:
    """Use case for getting shipping options"""

    def __init__(self, shipping_payment_repository: ShippingPaymentRepositoryInterface):
        self.repository = shipping_payment_repository

    def execute(self) -> List[Shipping]:
        """
        Get all shipping options
        
        Returns:
            List of Shipping entities
        """
        return self.repository.get_all_shippings()


class GetPaymentOptionsUseCase:
    """Use case for getting payment options"""

    def __init__(self, shipping_payment_repository: ShippingPaymentRepositoryInterface):
        self.repository = shipping_payment_repository

    def execute(self) -> List[Payment]:
        """
        Get all payment options
        
        Returns:
            List of Payment entities
        """
        return self.repository.get_all_payments()
