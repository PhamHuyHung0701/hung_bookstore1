import sqlite3

conn = sqlite3.connect('shared_db.sqlite3')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()
print("Tables in database:")
for t in tables:
    print(f"  - {t[0]}")

# Check books table
print("\nBooks in 'books' table:")
try:
    cursor.execute("SELECT * FROM books LIMIT 5")
    books = cursor.fetchall()
    for book in books:
        print(f"  {book}")
except Exception as e:
    print(f"  Error: {e}")

# Check hung_bookstore1_book table
print("\nBooks in 'hung_bookstore1_book' table:")
try:
    cursor.execute("SELECT * FROM hung_bookstore1_book LIMIT 5")
    books = cursor.fetchall()
    for book in books:
        print(f"  {book}")
except Exception as e:
    print(f"  Error: {e}")

conn.close()
