"""
Customer Controller - Interface Adapter Layer
Handles HTTP request/response and coordinates with Use Cases
"""
from typing import Dict, Any, Optional

from ...usecases.customer_usecases import (
    RegisterCustomerUseCase,
    LoginCustomerUseCase,
    GetCustomerProfileUseCase
)
from ...infrastructure.repositories.customer_repository_impl import DjangoCustomerRepository


class CustomerController:
    """Controller for customer-related operations"""

    def __init__(self):
        self.customer_repository = DjangoCustomerRepository()

    def register(self, name: str, email: str, password: str, 
                 confirm_password: str) -> Dict[str, Any]:
        """
        Handle customer registration
        
        Returns:
            Dict with 'success', 'message', and optionally 'customer'
        """
        try:
            use_case = RegisterCustomerUseCase(self.customer_repository)
            customer = use_case.execute(name, email, password, confirm_password)
            return {
                'success': True,
                'message': 'Đăng ký thành công! Vui lòng đăng nhập.',
                'customer': customer.to_dict()
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Handle customer login
        
        Returns:
            Dict with 'success', 'message', and optionally 'customer'
        """
        try:
            use_case = LoginCustomerUseCase(self.customer_repository)
            customer = use_case.execute(email, password)
            return {
                'success': True,
                'message': f'Chào mừng {customer.name}!',
                'customer': customer
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }

    def get_profile(self, customer_id: int) -> Dict[str, Any]:
        """
        Get customer profile
        
        Returns:
            Dict with 'success' and optionally 'customer'
        """
        use_case = GetCustomerProfileUseCase(self.customer_repository)
        customer = use_case.execute(customer_id)

        if customer:
            return {
                'success': True,
                'customer': customer
            }
        return {
            'success': False,
            'message': 'Không tìm thấy thông tin khách hàng'
        }
