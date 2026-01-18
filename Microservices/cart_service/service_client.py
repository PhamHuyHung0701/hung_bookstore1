"""
Cart Service - Service Client for calling other microservices
"""
import requests
from django.conf import settings


class ServiceClient:
    """Client for calling other microservices via REST APIs"""
    
    # Service URLs (configurable in settings)
    CUSTOMER_SERVICE_URL = getattr(settings, 'CUSTOMER_SERVICE_URL', 'http://localhost:8000/api/customers')
    BOOK_SERVICE_URL = getattr(settings, 'BOOK_SERVICE_URL', 'http://localhost:8000/api/books')
    
    @classmethod
    def check_customer_exists(cls, customer_id):
        """Check if customer exists in customer_service"""
        try:
            response = requests.get(
                f"{cls.CUSTOMER_SERVICE_URL}/{customer_id}/exists/",
                timeout=5
            )
            if response.status_code == 200:
                return response.json().get('exists', False)
            return False
        except requests.RequestException:
            # If service is unavailable, assume customer exists (for development)
            return True

    @classmethod
    def get_customer(cls, customer_id):
        """Get customer data from customer_service"""
        try:
            response = requests.get(
                f"{cls.CUSTOMER_SERVICE_URL}/{customer_id}/",
                timeout=5
            )
            if response.status_code == 200:
                return response.json().get('customer')
            return None
        except requests.RequestException:
            return None

    @classmethod
    def get_book(cls, book_id):
        """Get book data from book_service"""
        try:
            response = requests.get(
                f"{cls.BOOK_SERVICE_URL}/{book_id}/",
                timeout=5
            )
            if response.status_code == 200:
                return response.json().get('book')
            return None
        except requests.RequestException:
            return None

    @classmethod
    def check_book_stock(cls, book_id):
        """Check book stock from book_service"""
        try:
            response = requests.get(
                f"{cls.BOOK_SERVICE_URL}/{book_id}/stock/",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None

    @classmethod
    def update_book_stock(cls, book_id, quantity_change):
        """Update book stock in book_service"""
        try:
            response = requests.put(
                f"{cls.BOOK_SERVICE_URL}/{book_id}/update-stock/",
                json={'quantity': quantity_change},
                timeout=5
            )
            return response.status_code == 200
        except requests.RequestException:
            return False
