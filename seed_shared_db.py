#!/usr/bin/env python
"""
Script để tạo dữ liệu test cho shared_db.sqlite3
Dữ liệu này sẽ được dùng chung cho cả 3 dự án:
- Monolithic
- Clean Architecture
- Microservices

Các chức năng được test:
1. Nhân viên nhập sách vào kho (Staff + Books)
2. Khách hàng tìm kiếm và xem sách (Customers + Books)
3. Tạo giỏ hàng và thêm sách (Carts + CartItems)
4. Đặt hàng (Orders + OrderItems)
5. Chọn phương thức thanh toán (Payments)
6. Chọn phương thức giao hàng (Shipping)
7. Gợi ý sách dựa trên lịch sử mua và rating (Ratings + Orders)
"""
import sqlite3
import os
from datetime import datetime, timedelta
import random

# Path to shared database
DB_PATH = r'd:\hung_bookstore1\shared_db.sqlite3'

def create_tables(conn):
    """Tạo các bảng cần thiết"""
    cursor = conn.cursor()
    
    # Drop existing tables
    tables = ['order_items', 'orders', 'cart_items', 'carts', 'ratings', 
              'payments', 'shipping', 'staff', 'books', 'customers',
              'django_session', 'django_migrations', 'django_content_type',
              'auth_permission', 'auth_group', 'auth_user']
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    
    # Create Django system tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS django_migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            applied DATETIME NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS django_session (
            session_key VARCHAR(40) PRIMARY KEY,
            session_data TEXT NOT NULL,
            expire_date DATETIME NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS django_content_type (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_label VARCHAR(100) NOT NULL,
            model VARCHAR(100) NOT NULL,
            UNIQUE (app_label, model)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auth_permission (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_type_id INTEGER NOT NULL,
            codename VARCHAR(100) NOT NULL,
            name VARCHAR(255) NOT NULL,
            FOREIGN KEY (content_type_id) REFERENCES django_content_type(id),
            UNIQUE (content_type_id, codename)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auth_group (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(150) UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auth_user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password VARCHAR(128) NOT NULL,
            last_login DATETIME,
            is_superuser BOOLEAN NOT NULL,
            username VARCHAR(150) UNIQUE NOT NULL,
            first_name VARCHAR(150) NOT NULL,
            last_name VARCHAR(150) NOT NULL,
            email VARCHAR(254) NOT NULL,
            is_staff BOOLEAN NOT NULL,
            is_active BOOLEAN NOT NULL,
            date_joined DATETIME NOT NULL
        )
    ''')
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    ''')
    
    # Create books table
    cursor.execute('''
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(200) NOT NULL,
            author VARCHAR(100) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            stock_quantity INTEGER DEFAULT 0
        )
    ''')
    
    # Create staff table
    cursor.execute('''
        CREATE TABLE staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            role VARCHAR(50) NOT NULL
        )
    ''')
    
    # Create ratings table
    cursor.execute('''
        CREATE TABLE ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (book_id) REFERENCES books(id),
            UNIQUE (customer_id, book_id)
        )
    ''')
    
    # Create carts table
    cursor.execute('''
        CREATE TABLE carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    ''')
    
    # Create cart_items table
    cursor.execute('''
        CREATE TABLE cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cart_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (cart_id) REFERENCES carts(id),
            FOREIGN KEY (book_id) REFERENCES books(id),
            UNIQUE (cart_id, book_id)
        )
    ''')
    
    # Create shipping table
    cursor.execute('''
        CREATE TABLE shipping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method_name VARCHAR(120) NOT NULL,
            fee DECIMAL(8, 2) NOT NULL
        )
    ''')
    
    # Create payments table
    cursor.execute('''
        CREATE TABLE payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method_name VARCHAR(120) NOT NULL,
            status VARCHAR(50) DEFAULT 'pending'
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            total_price DECIMAL(12, 2) NOT NULL,
            shipping_id INTEGER,
            payment_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (shipping_id) REFERENCES shipping(id),
            FOREIGN KEY (payment_id) REFERENCES payments(id)
        )
    ''')
    
    # Create order_items table
    cursor.execute('''
        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    ''')
    
    conn.commit()
    print("✓ Đã tạo tất cả các bảng")

def seed_customers(conn):
    """Tạo dữ liệu khách hàng"""
    cursor = conn.cursor()
    
    customers = [
        ('Nguyễn Văn An', 'an@example.com', 'password123'),
        ('Trần Thị Bình', 'binh@example.com', 'password123'),
        ('Lê Hoàng Cường', 'cuong@example.com', 'password123'),
        ('Phạm Minh Dũng', 'dung@example.com', 'password123'),
        ('Hoàng Thị Hà', 'ha@example.com', 'password123'),
        ('Vũ Quang Huy', 'huy@example.com', 'password123'),
        ('Đặng Thị Lan', 'lan@example.com', 'password123'),
        ('Bùi Văn Nam', 'nam@example.com', 'password123'),        ('test', 'test@example.com', 'test'),  # Test account đơn giản
    ]
    
    cursor.executemany(
        'INSERT INTO customers (name, email, password) VALUES (?, ?, ?)',
        customers
    )
    conn.commit()
    print(f"✓ Đã tạo {len(customers)} khách hàng")
    return len(customers)

def seed_staff(conn):
    """Tạo dữ liệu nhân viên"""
    cursor = conn.cursor()
    
    staff = [
        ('Nguyễn Văn Manager', 'Manager'),
        ('Trần Thị Clerk', 'Clerk'),
        ('Lê Inventory', 'Inventory Specialist'),
        ('Phạm Cashier', 'Cashier'),
        ('staff', 'Staff'),  # Test staff account
    ]
    
    cursor.executemany(
        'INSERT INTO staff (name, role) VALUES (?, ?)',
        staff
    )
    conn.commit()
    print(f"✓ Đã tạo {len(staff)} nhân viên")

def seed_books(conn):
    """Tạo dữ liệu sách"""
    cursor = conn.cursor()
    
    books = [
        # Sách Việt Nam
        ('Truyện Kiều', 'Nguyễn Du', 89000, 50),
        ('Số Đỏ', 'Vũ Trọng Phụng', 75000, 30),
        ('Tắt Đèn', 'Ngô Tất Tố', 65000, 40),
        ('Dế Mèn Phiêu Lưu Ký', 'Tô Hoài', 55000, 60),
        ('Nhật Ký Trong Tù', 'Hồ Chí Minh', 45000, 80),
        
        # Sách Tiếng Anh dịch
        ('Đắc Nhân Tâm', 'Dale Carnegie', 95000, 100),
        ('Nhà Giả Kim', 'Paulo Coelho', 79000, 70),
        ('Sapiens - Lược Sử Loài Người', 'Yuval Noah Harari', 199000, 25),
        ('Atomic Habits', 'James Clear', 159000, 45),
        ('Rich Dad Poor Dad', 'Robert Kiyosaki', 129000, 55),
        
        # Sách IT/Lập trình
        ('Clean Code', 'Robert C. Martin', 450000, 20),
        ('Design Patterns', 'Gang of Four', 520000, 15),
        ('The Pragmatic Programmer', 'David Thomas', 380000, 18),
        ('Python Crash Course', 'Eric Matthes', 320000, 35),
        ('JavaScript: The Good Parts', 'Douglas Crockford', 280000, 25),
        
        # Sách Văn học kinh điển
        ('1984', 'George Orwell', 125000, 40),
        ('To Kill a Mockingbird', 'Harper Lee', 115000, 35),
        ('The Great Gatsby', 'F. Scott Fitzgerald', 99000, 30),
        ('Pride and Prejudice', 'Jane Austen', 89000, 45),
        ('Harry Potter tập 1', 'J.K. Rowling', 165000, 100),
    ]
    
    cursor.executemany(
        'INSERT INTO books (title, author, price, stock_quantity) VALUES (?, ?, ?, ?)',
        books
    )
    conn.commit()
    print(f"✓ Đã tạo {len(books)} sách")
    return len(books)

def seed_shipping(conn):
    """Tạo dữ liệu phương thức giao hàng"""
    cursor = conn.cursor()
    
    shipping_methods = [
        ('Giao hàng tiêu chuẩn (3-5 ngày)', 25000),
        ('Giao hàng nhanh (1-2 ngày)', 45000),
        ('Giao hàng hỏa tốc (trong ngày)', 65000),
        ('Nhận tại cửa hàng', 0),
        ('Giao hàng COD', 30000),
    ]
    
    cursor.executemany(
        'INSERT INTO shipping (method_name, fee) VALUES (?, ?)',
        shipping_methods
    )
    conn.commit()
    print(f"✓ Đã tạo {len(shipping_methods)} phương thức giao hàng")

def seed_payments(conn):
    """Tạo dữ liệu phương thức thanh toán"""
    cursor = conn.cursor()
    
    payment_methods = [
        ('Thanh toán khi nhận hàng (COD)', 'active'),
        ('Chuyển khoản ngân hàng', 'active'),
        ('Ví MoMo', 'active'),
        ('Ví ZaloPay', 'active'),
        ('Thẻ tín dụng/ghi nợ (Visa/Mastercard)', 'active'),
        ('VNPay', 'active'),
    ]
    
    cursor.executemany(
        'INSERT INTO payments (method_name, status) VALUES (?, ?)',
        payment_methods
    )
    conn.commit()
    print(f"✓ Đã tạo {len(payment_methods)} phương thức thanh toán")

def seed_ratings(conn, num_customers, num_books):
    """Tạo dữ liệu đánh giá sách"""
    cursor = conn.cursor()
    
    ratings_count = 0
    used_pairs = set()
    
    # Tạo ratings ngẫu nhiên nhưng đảm bảo không trùng
    for _ in range(50):
        customer_id = random.randint(1, num_customers)
        book_id = random.randint(1, num_books)
        
        if (customer_id, book_id) not in used_pairs:
            score = random.randint(1, 5)
            try:
                cursor.execute(
                    'INSERT INTO ratings (customer_id, book_id, score) VALUES (?, ?, ?)',
                    (customer_id, book_id, score)
                )
                used_pairs.add((customer_id, book_id))
                ratings_count += 1
            except:
                pass
    
    conn.commit()
    print(f"✓ Đã tạo {ratings_count} đánh giá sách")

def seed_carts(conn, num_customers, num_books):
    """Tạo dữ liệu giỏ hàng"""
    cursor = conn.cursor()
    
    cart_count = 0
    item_count = 0
    
    # Tạo cart cho một số khách hàng
    for customer_id in range(1, num_customers + 1):
        if random.random() > 0.3:  # 70% khách hàng có giỏ hàng
            cursor.execute(
                'INSERT INTO carts (customer_id, is_active) VALUES (?, ?)',
                (customer_id, True)
            )
            cart_id = cursor.lastrowid
            cart_count += 1
            
            # Thêm sách vào giỏ hàng
            num_items = random.randint(1, 4)
            used_books = set()
            for _ in range(num_items):
                book_id = random.randint(1, num_books)
                if book_id not in used_books:
                    quantity = random.randint(1, 3)
                    cursor.execute(
                        'INSERT INTO cart_items (cart_id, book_id, quantity) VALUES (?, ?, ?)',
                        (cart_id, book_id, quantity)
                    )
                    used_books.add(book_id)
                    item_count += 1
    
    conn.commit()
    print(f"✓ Đã tạo {cart_count} giỏ hàng với {item_count} sản phẩm")

def seed_orders(conn, num_customers, num_books):
    """Tạo dữ liệu đơn hàng (lịch sử mua hàng)"""
    cursor = conn.cursor()
    
    order_count = 0
    item_count = 0
    
    # Lấy số lượng shipping và payment
    cursor.execute('SELECT COUNT(*) FROM shipping')
    num_shipping = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM payments')
    num_payments = cursor.fetchone()[0]
    
    # Tạo orders cho các khách hàng
    for customer_id in range(1, num_customers + 1):
        # Mỗi khách hàng có 0-3 đơn hàng
        num_orders = random.randint(0, 3)
        
        for _ in range(num_orders):
            shipping_id = random.randint(1, num_shipping)
            payment_id = random.randint(1, num_payments)
            
            # Lấy phí ship
            cursor.execute('SELECT fee FROM shipping WHERE id = ?', (shipping_id,))
            shipping_fee = cursor.fetchone()[0]
            
            # Tính total price
            total_price = float(shipping_fee)
            
            # Tạo order trước
            created_at = datetime.now() - timedelta(days=random.randint(1, 90))
            cursor.execute(
                '''INSERT INTO orders (customer_id, total_price, shipping_id, payment_id, created_at) 
                   VALUES (?, ?, ?, ?, ?)''',
                (customer_id, 0, shipping_id, payment_id, created_at)
            )
            order_id = cursor.lastrowid
            order_count += 1
            
            # Thêm order items
            num_items = random.randint(1, 5)
            used_books = set()
            order_total = float(shipping_fee)
            
            for _ in range(num_items):
                book_id = random.randint(1, num_books)
                if book_id not in used_books:
                    # Lấy giá sách
                    cursor.execute('SELECT price FROM books WHERE id = ?', (book_id,))
                    book_price = cursor.fetchone()[0]
                    
                    quantity = random.randint(1, 2)
                    cursor.execute(
                        'INSERT INTO order_items (order_id, book_id, quantity, price) VALUES (?, ?, ?, ?)',
                        (order_id, book_id, quantity, book_price)
                    )
                    order_total += float(book_price) * quantity
                    used_books.add(book_id)
                    item_count += 1
            
            # Cập nhật total price của order
            cursor.execute('UPDATE orders SET total_price = ? WHERE id = ?', (order_total, order_id))
    
    conn.commit()
    print(f"✓ Đã tạo {order_count} đơn hàng với {item_count} sản phẩm")

def main():
    print("=" * 60)
    print("SEED DỮ LIỆU TEST CHO SHARED_DB.SQLITE3")
    print("=" * 60)
    print()
    
    # Xóa file database cũ nếu tồn tại
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"✓ Đã xóa database cũ: {DB_PATH}")
    
    # Kết nối database
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Tạo tables
        create_tables(conn)
        
        # Seed data
        print("\n--- Tạo dữ liệu test ---")
        seed_customers(conn)
        seed_staff(conn)
        num_books = seed_books(conn)
        seed_shipping(conn)
        seed_payments(conn)
        seed_ratings(conn, 9, num_books)  # 9 customers
        seed_carts(conn, 9, num_books)
        seed_orders(conn, 9, num_books)
        
        print("\n" + "=" * 60)
        print("✓ HOÀN THÀNH TẠO DỮ LIỆU TEST!")
        print("=" * 60)
        
        # Thống kê
        print("\n--- Thống kê dữ liệu ---")
        cursor = conn.cursor()
        tables = ['customers', 'staff', 'books', 'ratings', 'carts', 'cart_items', 
                  'orders', 'order_items', 'shipping', 'payments']
        for table in tables:
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            count = cursor.fetchone()[0]
            print(f"  {table}: {count} records")
        
        print("\n--- Tài khoản test ---")
        print("  Customer: test@example.com / test")
        print("  Staff: staff@bookstore.com / staff")
        
    finally:
        conn.close()

if __name__ == '__main__':
    main()
