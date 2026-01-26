"""
Shipping and Payment Repository Implementation - Django ORM
"""
from typing import List
from decimal import Decimal

from ...domain.entities.shipping_payment import Shipping, Payment
from ...domain.repositories.shipping_payment_repository import ShippingPaymentRepositoryInterface
from ..orm.models import ShippingModel, PaymentModel


class DjangoShippingPaymentRepository(ShippingPaymentRepositoryInterface):
    """Django ORM implementation of Shipping and Payment Repository"""

    def get_all_shippings(self) -> List[Shipping]:
        """Get all shipping options"""
        models = ShippingModel.objects.all()
        return [Shipping(
            id=model.id,
            method_name=model.method_name,
            fee=Decimal(str(model.fee))
        ) for model in models]

    def get_all_payments(self) -> List[Payment]:
        """Get all payment options"""
        models = PaymentModel.objects.all()
        return [Payment(
            id=model.id,
            method_name=model.method_name,
            status=model.status
        ) for model in models]
