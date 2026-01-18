"""
Cart Repository Implementation - Django ORM
"""
from typing import Optional, List
from decimal import Decimal

from ...domain.entities.cart import Cart, CartItem
from ...domain.entities.book import Book
from ...domain.repositories.cart_repository import CartRepositoryInterface
from ..orm.models import CartModel, CartItemModel, BookModel, CustomerModel


class DjangoCartRepository(CartRepositoryInterface):
    """Django ORM implementation of Cart Repository"""

    def _book_to_entity(self, model: BookModel) -> Book:
        """Convert Book ORM model to domain entity"""
        return Book(
            id=model.id,
            title=model.title,
            author=model.author,
            price=Decimal(str(model.price)),
            stock=model.stock,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _cart_item_to_entity(self, model: CartItemModel) -> CartItem:
        """Convert CartItem ORM model to domain entity"""
        return CartItem(
            id=model.id,
            cart_id=model.cart_id,
            book_id=model.book_id,
            book=self._book_to_entity(model.book),
            quantity=model.quantity,
            added_at=model.added_at
        )

    def _cart_to_entity(self, model: CartModel, include_items: bool = True) -> Cart:
        """Convert Cart ORM model to domain entity"""
        items = []
        if include_items:
            item_models = model.items.all()
            items = [self._cart_item_to_entity(item) for item in item_models]

        return Cart(
            id=model.id,
            customer_id=model.customer_id,
            items=items,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def get_by_customer_id(self, customer_id: int) -> Optional[Cart]:
        """Get cart by customer ID"""
        try:
            model = CartModel.objects.get(customer_id=customer_id)
            return self._cart_to_entity(model)
        except CartModel.DoesNotExist:
            return None

    def get_or_create(self, customer_id: int) -> Cart:
        """Get existing cart or create new one for customer"""
        try:
            customer = CustomerModel.objects.get(id=customer_id)
            model, created = CartModel.objects.get_or_create(customer=customer)
            return self._cart_to_entity(model)
        except CustomerModel.DoesNotExist:
            raise ValueError("Customer not found")

    def add_item(self, cart_id: int, book_id: int, quantity: int) -> CartItem:
        """Add item to cart"""
        cart = CartModel.objects.get(id=cart_id)
        book = BookModel.objects.get(id=book_id)

        # Check if item already exists
        try:
            item = CartItemModel.objects.get(cart=cart, book=book)
            # Update quantity
            if item.quantity + quantity <= book.stock:
                item.quantity += quantity
                item.save()
            return self._cart_item_to_entity(item)
        except CartItemModel.DoesNotExist:
            # Create new item
            item = CartItemModel.objects.create(
                cart=cart,
                book=book,
                quantity=quantity
            )
            return self._cart_item_to_entity(item)

    def update_item_quantity(self, item_id: int, quantity: int) -> Optional[CartItem]:
        """Update cart item quantity"""
        try:
            item = CartItemModel.objects.get(id=item_id)
            item.quantity = quantity
            item.save()
            return self._cart_item_to_entity(item)
        except CartItemModel.DoesNotExist:
            return None

    def remove_item(self, item_id: int) -> bool:
        """Remove item from cart"""
        try:
            item = CartItemModel.objects.get(id=item_id)
            item.delete()
            return True
        except CartItemModel.DoesNotExist:
            return False

    def get_cart_item(self, item_id: int) -> Optional[CartItem]:
        """Get cart item by ID"""
        try:
            item = CartItemModel.objects.get(id=item_id)
            return self._cart_item_to_entity(item)
        except CartItemModel.DoesNotExist:
            return None

    def get_cart_items(self, cart_id: int) -> List[CartItem]:
        """Get all items in a cart"""
        items = CartItemModel.objects.filter(cart_id=cart_id)
        return [self._cart_item_to_entity(item) for item in items]
