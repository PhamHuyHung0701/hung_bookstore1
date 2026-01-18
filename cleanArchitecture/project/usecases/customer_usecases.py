"""
Customer Use Cases - Application Business Rules
"""
from typing import Optional
from django.contrib.auth.hashers import make_password, check_password

from ..domain.entities.customer import Customer
from ..domain.repositories.customer_repository import CustomerRepositoryInterface


class RegisterCustomerUseCase:
    """Use case for customer registration"""

    def __init__(self, customer_repository: CustomerRepositoryInterface):
        self.customer_repository = customer_repository

    def execute(self, name: str, email: str, password: str, confirm_password: str) -> Customer:
        """
        Register a new customer
        
        Args:
            name: Customer's name
            email: Customer's email
            password: Customer's password
            confirm_password: Password confirmation
            
        Returns:
            Created Customer entity
            
        Raises:
            ValueError: If validation fails
        """
        # Validate password confirmation
        if password != confirm_password:
            raise ValueError("Mật khẩu xác nhận không khớp!")

        # Check if email already exists
        if self.customer_repository.exists_by_email(email):
            raise ValueError("Email đã được sử dụng!")

        # Create customer entity
        customer = Customer(
            name=name,
            email=email,
            password=password
        )

        # Validate customer data
        customer.validate()

        # Hash password before saving
        customer.password = make_password(password)

        # Save and return
        return self.customer_repository.create(customer)


class LoginCustomerUseCase:
    """Use case for customer login"""

    def __init__(self, customer_repository: CustomerRepositoryInterface):
        self.customer_repository = customer_repository

    def execute(self, email: str, password: str) -> Customer:
        """
        Authenticate customer login
        
        Args:
            email: Customer's email
            password: Customer's password
            
        Returns:
            Authenticated Customer entity
            
        Raises:
            ValueError: If authentication fails
        """
        customer = self.customer_repository.get_by_email(email)

        if not customer:
            raise ValueError("Email không tồn tại!")

        if not check_password(password, customer.password):
            raise ValueError("Mật khẩu không đúng!")

        return customer


class GetCustomerProfileUseCase:
    """Use case for getting customer profile"""

    def __init__(self, customer_repository: CustomerRepositoryInterface):
        self.customer_repository = customer_repository

    def execute(self, customer_id: int) -> Optional[Customer]:
        """
        Get customer profile by ID
        
        Args:
            customer_id: Customer's ID
            
        Returns:
            Customer entity or None
        """
        return self.customer_repository.get_by_id(customer_id)
