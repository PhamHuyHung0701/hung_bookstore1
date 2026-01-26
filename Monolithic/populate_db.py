#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hung_bookstore1.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from book.models import Book, Rating, Staff
from customer.models import Customer
from cart.models import Cart, CartItem, Order, OrderItem, Shipping, Payment
import random

def create_test_data():
    # Clear existing data
    Book.objects.all().delete()
    Customer.objects.all().delete()
    Staff.objects.all().delete()
    Rating.objects.all().delete()
    Cart.objects.all().delete()
    CartItem.objects.all().delete()
    Order.objects.all().delete()
    OrderItem.objects.all().delete()
    Shipping.objects.all().delete()
    Payment.objects.all().delete()

    # Create sample books
    books_data = [
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'price': 15.99, 'stock_quantity': 50},
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'price': 12.99, 'stock_quantity': 40},
        {'title': '1984', 'author': 'George Orwell', 'price': 14.99, 'stock_quantity': 60},
        {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'price': 11.99, 'stock_quantity': 30},
        {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'price': 13.99, 'stock_quantity': 45},
        {'title': 'Harry Potter and the Sorcerer\'s Stone', 'author': 'J.K. Rowling', 'price': 16.99, 'stock_quantity': 70},
        {'title': 'The Lord of the Rings', 'author': 'J.R.R. Tolkien', 'price': 25.99, 'stock_quantity': 25},
        {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'price': 18.99, 'stock_quantity': 35},
        {'title': 'Dune', 'author': 'Frank Herbert', 'price': 19.99, 'stock_quantity': 40},
        {'title': 'Neuromancer', 'author': 'William Gibson', 'price': 17.99, 'stock_quantity': 20},
    ]

    books = []
    for data in books_data:
        book = Book.objects.create(**data)
        books.append(book)
    print(f'✓ Created {len(books)} books')

    # Create sample customers
    customers_data = [
        {'name': 'Alice Johnson', 'email': 'alice@example.com', 'password': 'password123'},
        {'name': 'Bob Smith', 'email': 'bob@example.com', 'password': 'password123'},
        {'name': 'Charlie Brown', 'email': 'charlie@example.com', 'password': 'password123'},
        {'name': 'Diana Prince', 'email': 'diana@example.com', 'password': 'password123'},
        {'name': 'Eve Wilson', 'email': 'eve@example.com', 'password': 'password123'},
    ]

    customers = []
    for data in customers_data:
        customer = Customer.objects.create(**data)
        customers.append(customer)
    print(f'✓ Created {len(customers)} customers')

    # Create sample staff
    staff_data = [
        {'name': 'Manager John', 'role': 'Manager'},
        {'name': 'Clerk Jane', 'role': 'Clerk'},
        {'name': 'Supervisor Mike', 'role': 'Supervisor'},
    ]

    staff_list = []
    for data in staff_data:
        staff = Staff.objects.create(**data)
        staff_list.append(staff)
    print(f'✓ Created {len(staff_list)} staff members')

    # Create sample ratings
    ratings_count = 0
    for _ in range(20):
        customer = random.choice(customers)
        book = random.choice(books)
        score = random.randint(1, 5)
        try:
            Rating.objects.create(customer=customer, book=book, score=score)
            ratings_count += 1
        except:
            pass
    print(f'✓ Created {ratings_count} ratings')

    # Create sample carts and cart items
    cart_items_count = 0
    for customer in customers:
        cart = Cart.objects.create(customer=customer, is_active=True)
        num_items = random.randint(1, 5)
        for _ in range(num_items):
            book = random.choice(books)
            quantity = random.randint(1, 3)
            CartItem.objects.create(cart=cart, book=book, quantity=quantity)
            cart_items_count += 1
    print(f'✓ Created carts and {cart_items_count} cart items')

    # Create sample orders
    order_items_count = 0
    for customer in customers:
        total_price = random.uniform(20, 100)
        order = Order.objects.create(customer=customer, total_price=round(total_price, 2))
        num_items = random.randint(1, 3)
        for _ in range(num_items):
            book = random.choice(books)
            quantity = random.randint(1, 2)
            price = book.price
            OrderItem.objects.create(order=order, book=book, quantity=quantity, price=price)
            order_items_count += 1
    print(f'✓ Created orders and {order_items_count} order items')

    # Create sample shipping and payment methods
    shipping_data = [
        {'method_name': 'Standard Shipping', 'fee': 5.99},
        {'method_name': 'Express Shipping', 'fee': 12.99},
        {'method_name': 'Overnight Shipping', 'fee': 24.99},
    ]

    for data in shipping_data:
        Shipping.objects.create(**data)
    print(f'✓ Created {len(shipping_data)} shipping methods')

    payment_data = [
        {'method_name': 'Credit Card', 'status': 'Active'},
        {'method_name': 'Debit Card', 'status': 'Active'},
        {'method_name': 'PayPal', 'status': 'Active'},
        {'method_name': 'Bank Transfer', 'status': 'Active'},
    ]

    for data in payment_data:
        Payment.objects.create(**data)
    print(f'✓ Created {len(payment_data)} payment methods')

    print('\n✅ Sample data added to Monolithic database successfully!')

if __name__ == '__main__':
    create_test_data()
