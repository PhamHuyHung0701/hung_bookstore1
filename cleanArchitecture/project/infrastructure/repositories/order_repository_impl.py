"""
Order Repository Implementation - Django ORM
"""
from typing import Optional, List
from decimal import Decimal

from ...domain.entities.order import Order, OrderItem
from ...domain.repositories.order_repository import OrderRepositoryInterface
from ..orm.models import OrderModel, OrderItemModel


class DjangoOrderRepository(OrderRepositoryInterface):
    """Django ORM implementation of Order Repository"""

    def _order_to_entity(self, model: OrderModel) -> Order:
        """Convert Order ORM model to domain entity"""
        items = []
        for item_model in model.items.all():
            item = OrderItem(
                id=item_model.id,
                order_id=item_model.order_id,
                book_id=item_model.book_id,
                quantity=item_model.quantity,
                price=Decimal(str(item_model.price))
            )
            items.append(item)
        
        return Order(
            id=model.id,
            customer_id=model.customer_id,
            total_price=Decimal(str(model.total_price)),
            shipping_id=model.shipping_id,
            payment_id=model.payment_id,
            created_at=model.created_at,
            items=items
        )

    def create(self, customer_id: int, total_price: float, shipping_id: int, payment_id: int) -> Order:
        """Create a new order"""
        model = OrderModel.objects.create(
            customer_id=customer_id,
            total_price=total_price,
            shipping_id=shipping_id,
            payment_id=payment_id
        )
        return self._order_to_entity(model)

    def get_by_customer_id(self, customer_id: int) -> List[Order]:
        """Get orders by customer ID"""
        models = OrderModel.objects.filter(customer_id=customer_id).order_by('-id')
        return [self._order_to_entity(m) for m in models]

    def add_item(self, order_id: int, book_id: int, quantity: int, price: float) -> None:
        """Add item to order"""
        OrderItemModel.objects.create(
            order_id=order_id,
            book_id=book_id,
            quantity=quantity,
            price=price
        )
