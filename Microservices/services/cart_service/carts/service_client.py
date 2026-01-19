"""
Service Client for Cart Service
Communicates with Customer Service and Book Service via HTTP
"""
import requests
from django.conf import settings


class ServiceClient:
    """Client for accessing other microservices via REST API"""
    
    CUSTOMER_SERVICE_URL = getattr(settings, 'CUSTOMER_SERVICE_URL', 'http://localhost:8001')
    BOOK_SERVICE_URL = getattr(settings, 'BOOK_SERVICE_URL', 'http://localhost:8002')
    
    @classmethod
    def check_customer_exists(cls, customer_id):
        """Check if customer exists by calling Customer Service"""
        try:
            response = requests.get(
                f"{cls.CUSTOMER_SERVICE_URL}/api/customers/{customer_id}/exists/",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('exists', False)
            return False
        except requests.RequestException as e:
            print(f"Error connecting to Customer Service: {e}")
            return False

    @classmethod
    def get_customer(cls, customer_id):
        """Get customer data from Customer Service"""
        try:
            response = requests.get(
                f"{cls.CUSTOMER_SERVICE_URL}/api/customers/{customer_id}/",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('customer')
            return None
        except requests.RequestException as e:
            print(f"Error connecting to Customer Service: {e}")
            return None

    @classmethod
    def get_book(cls, book_id):
        """Get book data from Book Service"""
        try:
            response = requests.get(
                f"{cls.BOOK_SERVICE_URL}/api/books/{book_id}/",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('book')
            return None
        except requests.RequestException as e:
            print(f"Error connecting to Book Service: {e}")
            return None

    @classmethod
    def check_book_stock(cls, book_id):
        """Check book stock from Book Service"""
        try:
            response = requests.get(
                f"{cls.BOOK_SERVICE_URL}/api/books/{book_id}/stock/",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException as e:
            print(f"Error connecting to Book Service: {e}")
            return None

    @classmethod
    def update_book_stock(cls, book_id, quantity_change):
        """Update book stock via Book Service"""
        try:
            response = requests.post(
                f"{cls.BOOK_SERVICE_URL}/api/books/{book_id}/update-stock/",
                json={'quantity_change': quantity_change},
                timeout=5
            )
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Error connecting to Book Service: {e}")
            return False
