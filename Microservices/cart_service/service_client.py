"""
Cart Service - Service Client for accessing other microservices data

NOTE: In a real microservices architecture, each service runs on different ports.
Since we're running all services in the same Django project for demo purposes,
we access the models directly instead of making HTTP requests to avoid deadlock.
In production, you would use HTTP requests to different service URLs.
"""
from customer_service.models import Customer
from book_service.models import Book


class ServiceClient:
    """
    Client for accessing other microservices data.
    
    In a real microservices setup with separate servers, this would use HTTP requests.
    For this demo (single Django server), we access models directly to avoid deadlock.
    """
    
    @classmethod
    def check_customer_exists(cls, customer_id):
        """Check if customer exists"""
        try:
            return Customer.objects.filter(id=customer_id).exists()
        except Exception:
            return False

    @classmethod
    def get_customer(cls, customer_id):
        """Get customer data"""
        try:
            customer = Customer.objects.get(id=customer_id)
            return {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email
            }
        except Customer.DoesNotExist:
            return None

    @classmethod
    def get_book(cls, book_id):
        """Get book data"""
        try:
            book = Book.objects.get(id=book_id)
            return {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'price': float(book.price),
                'stock': book.stock
            }
        except Book.DoesNotExist:
            return None

    @classmethod
    def check_book_stock(cls, book_id):
        """Check book stock"""
        try:
            book = Book.objects.get(id=book_id)
            return {
                'book_id': book.id,
                'title': book.title,
                'stock': book.stock,
                'available': book.stock > 0
            }
        except Book.DoesNotExist:
            return None

    @classmethod
    def update_book_stock(cls, book_id, quantity_change):
        """Update book stock"""
        try:
            book = Book.objects.get(id=book_id)
            book.stock += quantity_change
            if book.stock < 0:
                book.stock = 0
            book.save()
            return True
        except Book.DoesNotExist:
            return False
