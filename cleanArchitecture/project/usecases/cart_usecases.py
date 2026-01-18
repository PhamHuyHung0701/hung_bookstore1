"""
Cart Use Cases - Application Business Rules
"""
from typing import Optional, List

from ..domain.entities.cart import Cart, CartItem
from ..domain.repositories.cart_repository import CartRepositoryInterface
from ..domain.repositories.book_repository import BookRepositoryInterface


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
