"""
Customer Repository Implementation - Django ORM
"""
from typing import Optional, List
from decimal import Decimal

from ...domain.entities.customer import Customer
from ...domain.repositories.customer_repository import CustomerRepositoryInterface
from ..orm.models import CustomerModel


class DjangoCustomerRepository(CustomerRepositoryInterface):
    """Django ORM implementation of Customer Repository"""

    def _to_entity(self, model: CustomerModel) -> Customer:
        """Convert ORM model to domain entity"""
        return Customer(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: Customer) -> CustomerModel:
        """Convert domain entity to ORM model"""
        model = CustomerModel(
            name=entity.name,
            email=entity.email,
            password=entity.password
        )
        if entity.id:
            model.id = entity.id
        return model

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """Get customer by ID"""
        try:
            model = CustomerModel.objects.get(id=customer_id)
            return self._to_entity(model)
        except CustomerModel.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email"""
        try:
            model = CustomerModel.objects.get(email=email)
            return self._to_entity(model)
        except CustomerModel.DoesNotExist:
            return None

    def create(self, customer: Customer) -> Customer:
        """Create a new customer"""
        model = CustomerModel(
            name=customer.name,
            email=customer.email,
            password=customer.password
        )
        model.save()
        return self._to_entity(model)

    def update(self, customer: Customer) -> Customer:
        """Update an existing customer"""
        model = CustomerModel.objects.get(id=customer.id)
        model.name = customer.name
        model.email = customer.email
        if customer.password:
            model.password = customer.password
        model.save()
        return self._to_entity(model)

    def delete(self, customer_id: int) -> bool:
        """Delete a customer"""
        try:
            model = CustomerModel.objects.get(id=customer_id)
            model.delete()
            return True
        except CustomerModel.DoesNotExist:
            return False

    def exists_by_email(self, email: str) -> bool:
        """Check if email already exists"""
        return CustomerModel.objects.filter(email=email).exists()
