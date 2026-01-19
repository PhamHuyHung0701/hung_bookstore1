"""
Service Client for API Gateway
Communicates with all microservices via HTTP
"""
import requests
from django.conf import settings


class ServiceClient:
    """Client for accessing all microservices via REST API"""
    
    CUSTOMER_SERVICE_URL = getattr(settings, 'CUSTOMER_SERVICE_URL', 'http://localhost:8001')
    BOOK_SERVICE_URL = getattr(settings, 'BOOK_SERVICE_URL', 'http://localhost:8002')
    CART_SERVICE_URL = getattr(settings, 'CART_SERVICE_URL', 'http://localhost:8003')
    
    # ============ Customer Service ============
    @classmethod
    def register_customer(cls, name, email, password, confirm_password):
        """Register new customer"""
        try:
            response = requests.post(
                f"{cls.CUSTOMER_SERVICE_URL}/api/customers/register/",
                json={
                    'name': name,
                    'email': email,
                    'password': password,
                    'confirm_password': confirm_password
                },
                timeout=5
            )
            return response.json(), response.status_code
        except requests.RequestException as e:
            return {'success': False, 'message': f'Lỗi kết nối Customer Service: {e}'}, 500

    @classmethod
    def login_customer(cls, email, password):
        """Login customer"""
        try:
            response = requests.post(
                f"{cls.CUSTOMER_SERVICE_URL}/api/customers/login/",
                json={'email': email, 'password': password},
                timeout=5
            )
            return response.json(), response.status_code
        except requests.RequestException as e:
            return {'success': False, 'message': f'Lỗi kết nối Customer Service: {e}'}, 500

    @classmethod
    def get_customer(cls, customer_id):
        """Get customer by ID"""
        try:
            response = requests.get(
                f"{cls.CUSTOMER_SERVICE_URL}/api/customers/{customer_id}/",
                timeout=5
            )
            return response.json(), response.status_code
        except requests.RequestException as e:
            return {'success': False, 'message': f'Lỗi kết nối Customer Service: {e}'}, 500

    # ============ Book Service ============
    @classmethod
    def get_all_books(cls):
        """Get all books"""
        try:
            response = requests.get(
                f"{cls.BOOK_SERVICE_URL}/api/books/",
                timeout=5
            )
            return response.json(), response.status_code
        except requests.RequestException as e:
            return {'success': False, 'message': f'Lỗi kết nối Book Service: {e}'}, 500

    @classmethod
    def get_book(cls, book_id):
        """Get book by ID"""
        try:
            response = requests.get(
                f"{cls.BOOK_SERVICE_URL}/api/books/{book_id}/",
                timeout=5
            )
            return response.json(), response.status_code
        except requests.RequestException as e:
            return {'success': False, 'message': f'Lỗi kết nối Book Service: {e}'}, 500

    @classmethod
    def check_book_stock(cls, book_id):
        """Check book stock"""
        try:
            response = requests.get(
                f"{cls.BOOK_SERVICE_URL}/api/books/{book_id}/stock/",
                timeout=5
            )
            return response.json(), response.status_code
        except requests.RequestException as e:
            return {'success': False, 'message': f'Lỗi kết nối Book Service: {e}'}, 500

    # ============ Cart Service ============
    @classmethod
    def get_cart(cls, customer_id):
        """Get customer's cart"""
        try:
            response = requests.get(
                f"{cls.CART_SERVICE_URL}/api/cart/{customer_id}/",
                timeout=5
            )
            return response.json(), response.status_code
        except requests.RequestException as e:
            return {'success': False, 'message': f'Lỗi kết nối Cart Service: {e}'}, 500

    @classmethod
    def add_to_cart(cls, customer_id, book_id, quantity=1):
        """Add book to cart"""
        try:
            response = requests.post(
                f"{cls.CART_SERVICE_URL}/api/cart/add/",
                json={
                    'customer_id': customer_id,
                    'book_id': book_id,
                    'quantity': quantity
                },
                timeout=5
            )
            return response.json(), response.status_code
        except requests.RequestException as e:
            return {'success': False, 'message': f'Lỗi kết nối Cart Service: {e}'}, 500

    @classmethod
    def remove_from_cart(cls, customer_id, item_id):
        """Remove item from cart"""
        try:
            response = requests.delete(
                f"{cls.CART_SERVICE_URL}/api/cart/{customer_id}/remove/{item_id}/",
                timeout=5
            )
            return response.json(), response.status_code
        except requests.RequestException as e:
            return {'success': False, 'message': f'Lỗi kết nối Cart Service: {e}'}, 500

    @classmethod
    def clear_cart(cls, customer_id):
        """Clear cart"""
        try:
            response = requests.delete(
                f"{cls.CART_SERVICE_URL}/api/cart/{customer_id}/clear/",
                timeout=5
            )
            return response.json(), response.status_code
        except requests.RequestException as e:
            return {'success': False, 'message': f'Lỗi kết nối Cart Service: {e}'}, 500
