# BÁO CÁO KIỂM TRA CHỨC NĂNG - BOOKSTORE PROJECTS

## 📋 DANH SÁCH CHỨC NĂNG YÊU CẦU

| # | Chức năng | Monolithic | Clean Architecture | Microservices |
|---|-----------|------------|-------------------|---------------|
| 1 | Nhân viên nhập sách vào kho | ✅ | ✅ | ✅ |
| 2 | Khách hàng tìm kiếm và xem sách | ✅ | ✅ | ✅ |
| 3 | Tạo giỏ hàng và thêm sách | ✅ | ✅ | ✅ |
| 4 | Đặt hàng | ✅ | ✅ | ✅ |
| 5 | Chọn phương thức thanh toán | ✅ | ✅ | ✅ |
| 6 | Chọn phương thức giao hàng (shipping) | ✅ | ✅ | ✅ |
| 7 | Gợi ý sách dựa trên lịch sử mua và rating | ✅ | ✅ | ✅ |

---

## 📁 CHI TIẾT TỪNG DỰ ÁN

### 1. MONOLITHIC (`d:\hung_bookstore1\Monolithic`)

#### Models:
- `book/models.py`: Book, Rating, Staff
- `cart/models.py`: Cart, CartItem, Order, OrderItem, Shipping, Payment
- `customer/models.py`: Customer

#### Views (Chức năng):
| Chức năng | File | Function |
|-----------|------|----------|
| Nhập sách vào kho | `book/views.py` | `add_stock()` |
| Tìm kiếm/xem sách | `book/views.py` | `catalog()`, `book_detail()` |
| Giỏ hàng | `cart/views.py` | `view_cart()`, `add_to_cart()` |
| Đặt hàng | `cart/views.py` | `checkout()` |
| Thanh toán | `cart/views.py` | `checkout()` với Payment |
| Giao hàng | `cart/views.py` | `checkout()` với Shipping |
| Gợi ý sách | `book/views.py` | `recommendations()` |

---

### 2. CLEAN ARCHITECTURE (`d:\hung_bookstore1\cleanArchitecture`)

#### Cấu trúc layers:
```
project/
├── domain/           # Entities, Repository interfaces
├── usecases/         # Business logic
├── interfaces/       # Controllers
├── infrastructure/   # ORM Models, Repository implementations
└── framework/        # Django views, templates, urls
```

#### Models (Infrastructure):
- `project/infrastructure/orm/models.py`: 
  - CustomerModel, BookModel, CartModel, CartItemModel
  - RatingModel, StaffModel, OrderModel, OrderItemModel
  - ShippingModel, PaymentModel

#### Views (Framework):
| Chức năng | File | Function |
|-----------|------|----------|
| Nhập sách vào kho | `framework/views/book_views.py` | `add_stock()` |
| Tìm kiếm/xem sách | `framework/views/book_views.py` | `catalog()`, `book_detail()` |
| Giỏ hàng | `framework/views/cart_views.py` | `view_cart()`, `add_to_cart()` |
| Đặt hàng | `framework/views/cart_views.py` | `checkout()` |
| Thanh toán | `framework/views/cart_views.py` | `checkout()` |
| Giao hàng | `framework/views/cart_views.py` | `checkout()` |
| Gợi ý sách | `framework/views/book_views.py` | `recommendations()` |

---

### 3. MICROSERVICES (`d:\hung_bookstore1\Microservices\services`)

#### Services:
| Service | Port | Chức năng |
|---------|------|-----------|
| Customer Service | 8001 | Quản lý khách hàng |
| Book Service | 8002 | Quản lý sách, ratings, staff |
| Cart Service | 8003 | Giỏ hàng, orders, shipping, payments |
| API Gateway | 8000 | Web interface, routing |

#### API Endpoints:

**Book Service (`book_service/books/views.py`):**
- `GET /api/books/` - Danh sách sách
- `GET /api/books/<id>/` - Chi tiết sách
- `POST /api/books/` - Thêm sách mới (Staff)
- `GET /api/books/<id>/stock/` - Kiểm tra tồn kho
- `POST /api/books/<id>/stock/` - Cập nhật tồn kho
- `GET /api/books/recommendations/` - Gợi ý sách

**Cart Service (`cart_service/carts/views.py`):**
- `GET /api/cart/<customer_id>/` - Xem giỏ hàng
- `POST /api/cart/add/` - Thêm vào giỏ
- `DELETE /api/cart/<customer_id>/remove/<item_id>/` - Xóa khỏi giỏ
- `PUT /api/cart/<customer_id>/update/<item_id>/` - Cập nhật số lượng
- `POST /api/cart/checkout/` - Đặt hàng
- `GET /api/cart/<customer_id>/orders/` - Lịch sử đơn hàng
- `GET /api/cart/shipping/` - Phương thức giao hàng
- `GET /api/cart/payment/` - Phương thức thanh toán

---

## 🗃️ DATABASE

### Shared Database: `d:\hung_bookstore1\shared_db.sqlite3`

#### Bảng dữ liệu:
| Bảng | Số records | Mô tả |
|------|------------|-------|
| customers | 9 | Khách hàng |
| staff | 5 | Nhân viên |
| books | 20 | Sách |
| ratings | 44 | Đánh giá sách |
| carts | 6 | Giỏ hàng |
| cart_items | 14 | Sản phẩm trong giỏ |
| orders | 11 | Đơn hàng |
| order_items | 29 | Sản phẩm trong đơn |
| shipping | 5 | Phương thức giao hàng |
| payments | 6 | Phương thức thanh toán |

#### Tài khoản test:
- **Customer:** test@example.com / test
- **Staff:** staff@bookstore.com / staff

**Lưu ý:** Tài khoản staff được hardcode trong code, không lưu trong database.

---

## 📂 CÁC FILE DB ĐÃ XÓA

Đã xóa các file db.sqlite3 thừa:
- ❌ `Monolithic/db.sqlite3`
- ❌ `cleanArchitecture/db.sqlite3`
- ❌ `Microservices/services/customer_service/db.sqlite3`
- ❌ `Microservices/services/book_service/db.sqlite3`
- ❌ `Microservices/services/cart_service/db.sqlite3`
- ❌ `Microservices/services/api_gateway/db.sqlite3`

**Chỉ giữ lại:** ✅ `shared_db.sqlite3`

---

## 🚀 HƯỚNG DẪN CHẠY

### Monolithic:
```bash
cd d:\hung_bookstore1\Monolithic
python manage.py runserver 8000
# Truy cập: http://localhost:8000
```

### Clean Architecture:
```bash
cd d:\hung_bookstore1\cleanArchitecture
python manage.py runserver 8000
# Truy cập: http://localhost:8000
```

### Microservices:
```bash
cd d:\hung_bookstore1\Microservices\services
start_all_services.bat
# Truy cập: http://localhost:8000 (API Gateway)
```

---

## ✅ KẾT LUẬN

Cả 3 dự án đều đã có đủ **7 chức năng** yêu cầu:
1. ✅ Nhân viên nhập sách vào kho
2. ✅ Khách hàng tìm kiếm và xem sách
3. ✅ Tạo giỏ hàng và thêm sách
4. ✅ Đặt hàng
5. ✅ Chọn phương thức thanh toán
6. ✅ Chọn phương thức giao hàng (shipping)
7. ✅ Gợi ý sách dựa trên lịch sử mua và rating

---

## 🔐 ĐỒNG BỘ ĐĂNG NHẬP

### Tất cả 3 dự án đã được đồng bộ:
- ✅ **Cùng form đăng nhập** cho cả Customer và Staff (login.html)
- ✅ **Tài khoản test:**
  - Customer: `test@example.com` / `test`
  - Staff: `staff@bookstore.com` / `staff`
- ✅ **Staff login riêng** (staff_login.html) cho từng dự án
- ✅ **Menu navigation** với các chức năng: Catalog, Recommendations, Order History

### Templates đã đồng bộ:
| Template | Monolithic | Clean Architecture | Microservices |
|----------|------------|-------------------|---------------|
| login.html | ✅ | ✅ | ✅ |
| staff_login.html | ✅ | ✅ | ✅ |
| add_stock.html | ✅ | ✅ | ✅ |
| checkout.html | ✅ | ✅ | ✅ |
| order_history.html | ✅ | ✅ | ✅ |
| recommendations.html | ✅ | ✅ | ✅ |
| base.html (navbar) | ✅ | ✅ | ✅ |
