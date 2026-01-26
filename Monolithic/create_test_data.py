import os
import sys
sys.path.insert(0, os.getcwd())
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hung_bookstore1.settings')
django.setup()

from book.models import Book, Rating, Staff
from customer.models import Customer
from cart.models import Cart, CartItem, Order, OrderItem, Shipping, Payment
import random

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

# Create sample ratings
for _ in range(20):
    customer = random.choice(customers)
    book = random.choice(books)
    score = random.randint(1, 5)
    Rating.objects.create(customer=customer, book=book, score=score)

# Create sample carts and cart items
for customer in customers:
    cart = Cart.objects.create(customer=customer, is_active=True)
    num_items = random.randint(1, 5)
    for _ in range(num_items):
        book = random.choice(books)
        quantity = random.randint(1, 3)
        CartItem.objects.create(cart=cart, book=book, quantity=quantity)

# Create sample orders
for customer in customers:
    total_price = random.uniform(20, 100)
    order = Order.objects.create(customer=customer, total_price=round(total_price, 2))
    num_items = random.randint(1, 3)
    for _ in range(num_items):
        book = random.choice(books)
        quantity = random.randint(1, 2)
        price = book.price
        OrderItem.objects.create(order=order, book=book, quantity=quantity, price=price)

print('Sample data added to Monolithic database.')
