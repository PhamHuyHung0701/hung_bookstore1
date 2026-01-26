"""
API Gateway Views - Web Interface
"""
from django.shortcuts import render, redirect
from django.contrib import messages

from .service_client import ServiceClient


def home(request):
    """Home page - Book catalog"""
    customer = None
    if request.session.get('customer_id'):
        data, status_code = ServiceClient.get_customer(request.session['customer_id'])
        if data.get('success'):
            customer = data.get('customer')
    
    # Get all books
    data, status_code = ServiceClient.get_all_books()
    books = []
    error = None
    
    if data.get('success'):
        books = data.get('books', [])
    else:
        error = data.get('message', 'Lỗi kết nối đến service')
    
    return render(request, 'gateway/home.html', {
        'books': books,
        'customer': customer,
        'error': error
    })


def register(request):
    """Customer registration page"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        data, status_code = ServiceClient.register_customer(
            name, email, password, confirm_password
        )
        
        if data.get('success'):
            messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
            return redirect('login')
        else:
            error = data.get('message') or data.get('errors', 'Đăng ký thất bại!')
            return render(request, 'gateway/register.html', {'error': error})
    
    return render(request, 'gateway/register.html')


def login(request):
    """Customer login page - hỗ trợ cả Customer và Staff"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Kiểm tra xem có phải tài khoản staff không
        if email == 'staff@bookstore.com' and password == 'staff':
            request.session['staff'] = True
            request.session['staff_email'] = email
            messages.success(request, 'Đăng nhập staff thành công!')
            return redirect('add_stock')
        
        # Nếu không phải staff, kiểm tra customer
        data, status_code = ServiceClient.login_customer(email, password)
        
        if data.get('success'):
            customer = data.get('customer')
            request.session['customer_id'] = customer['id']
            request.session['customer_name'] = customer['name']
            messages.success(request, f'Chào mừng {customer["name"]}!')
            return redirect('home')
        else:
            error = data.get('message', 'Đăng nhập thất bại!')
            return render(request, 'gateway/login.html', {'error': error})
    
    return render(request, 'gateway/login.html')


def logout(request):
    """Customer logout"""
    request.session.flush()
    messages.success(request, 'Đã đăng xuất!')
    return redirect('home')


def staff_login(request):
    """Staff login page"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Kiểm tra hardcoded staff account trước
        if email == 'staff@bookstore.com' and password == 'staff':
            request.session['staff'] = True
            request.session['staff_email'] = email
            messages.success(request, 'Đăng nhập staff thành công!')
            return redirect('add_stock')
        else:
            error = 'Thông tin đăng nhập không đúng!'
            return render(request, 'gateway/staff_login.html', {'error': error})
    
    return render(request, 'gateway/staff_login.html')


def staff_logout(request):
    """Staff logout"""
    request.session.pop('staff', None)
    messages.success(request, 'Đã đăng xuất staff!')
    return redirect('home')


def catalog(request):
    """Book catalog page"""
    customer = None
    if request.session.get('customer_id'):
        data, status_code = ServiceClient.get_customer(request.session['customer_id'])
        if data.get('success'):
            customer = data.get('customer')
    
    # Get all books
    data, status_code = ServiceClient.get_all_books()
    books = []
    error = None
    
    if data.get('success'):
        books = data.get('books', [])
    else:
        error = data.get('message', 'Lỗi kết nối đến service')
    
    return render(request, 'gateway/catalog.html', {
        'books': books,
        'customer': customer,
        'error': error
    })


def book_detail(request, book_id):
    """Book detail page"""
    customer = None
    if request.session.get('customer_id'):
        data, status_code = ServiceClient.get_customer(request.session['customer_id'])
        if data.get('success'):
            customer = data.get('customer')
    
    data, status_code = ServiceClient.get_book(book_id)
    
    if data.get('success'):
        book = data.get('book')
        return render(request, 'gateway/book_detail.html', {
            'book': book,
            'customer': customer
        })
    else:
        messages.error(request, 'Không tìm thấy sách!')
        return redirect('catalog')


def add_to_cart(request, book_id):
    """Add book to cart"""
    customer_id = request.session.get('customer_id')
    
    if not customer_id:
        messages.warning(request, 'Vui lòng đăng nhập để thêm sách vào giỏ hàng!')
        return redirect('login')
    
    quantity = int(request.GET.get('quantity', 1))
    
    data, status_code = ServiceClient.add_to_cart(customer_id, book_id, quantity)
    
    if data.get('success'):
        messages.success(request, 'Đã thêm sách vào giỏ hàng!')
    else:
        messages.error(request, data.get('message', 'Lỗi thêm sách vào giỏ hàng!'))
    
    return redirect('catalog')


def cart(request):
    """Cart page"""
    customer_id = request.session.get('customer_id')
    
    if not customer_id:
        messages.warning(request, 'Vui lòng đăng nhập để xem giỏ hàng!')
        return redirect('login')
    
    customer = None
    data, status_code = ServiceClient.get_customer(customer_id)
    if data.get('success'):
        customer = data.get('customer')
    
    data, status_code = ServiceClient.get_cart(customer_id)
    
    cart_data = None
    error = None
    
    if data.get('success'):
        cart_data = data.get('cart')
    else:
        error = data.get('message', 'Lỗi kết nối đến service')
    
    return render(request, 'gateway/cart.html', {
        'cart': cart_data,
        'customer': customer,
        'error': error
    })


def remove_from_cart(request, item_id):
    """Remove item from cart"""
    customer_id = request.session.get('customer_id')
    
    if not customer_id:
        messages.warning(request, 'Vui lòng đăng nhập!')
        return redirect('login')
    
    data, status_code = ServiceClient.remove_from_cart(customer_id, item_id)
    
    if data.get('success'):
        messages.success(request, 'Đã xóa sách khỏi giỏ hàng!')
    else:
        messages.error(request, data.get('message', 'Lỗi xóa sách!'))
    
    return redirect('cart')


def clear_cart(request):
    """Clear cart"""
    customer_id = request.session.get('customer_id')
    
    if not customer_id:
        messages.warning(request, 'Vui lòng đăng nhập!')
        return redirect('login')
    
    data, status_code = ServiceClient.clear_cart(customer_id)
    
    if data.get('success'):
        messages.success(request, 'Đã xóa toàn bộ giỏ hàng!')
    else:
        messages.error(request, data.get('message', 'Lỗi xóa giỏ hàng!'))
    
    return redirect('cart')


def update_cart_item(request, item_id):
    """Update cart item quantity"""
    customer_id = request.session.get('customer_id')
    
    if not customer_id:
        messages.warning(request, 'Vui lòng đăng nhập!')
        return redirect('login')
    
    quantity = int(request.POST.get('quantity', 1))
    
    data, status_code = ServiceClient.update_cart_item(customer_id, item_id, quantity)
    
    if data.get('success'):
        messages.success(request, 'Đã cập nhật số lượng!')
    else:
        messages.error(request, data.get('message', 'Lỗi cập nhật số lượng!'))
    
    return redirect('cart')


def checkout(request):
    """Checkout page"""
    customer_id = request.session.get('customer_id')
    
    if not customer_id:
        messages.warning(request, 'Vui lòng đăng nhập để thanh toán!')
        return redirect('login')
    
    if request.method == 'POST':
        shipping_id = request.POST.get('shipping_id')
        payment_id = request.POST.get('payment_id')
        
        data, status_code = ServiceClient.checkout(customer_id, shipping_id, payment_id)
        
        if data.get('success'):
            messages.success(request, 'Đặt hàng thành công!')
            return redirect('order_history')
        else:
            messages.error(request, data.get('message', 'Lỗi đặt hàng!'))
    
    # Get cart
    data, status_code = ServiceClient.get_cart(customer_id)
    cart_data = None
    if data.get('success'):
        cart_data = data.get('cart')
    
    # Get shipping and payment options
    shipping_data, _ = ServiceClient.get_shipping_options()
    payment_data, _ = ServiceClient.get_payment_options()
    
    shipping_options = shipping_data.get('shipping_options', []) if shipping_data.get('success') else []
    payment_options = payment_data.get('payment_options', []) if payment_data.get('success') else []
    
    return render(request, 'gateway/checkout.html', {
        'cart': cart_data,
        'shipping_options': shipping_options,
        'payment_options': payment_options
    })


def order_history(request):
    """Order history page"""
    customer_id = request.session.get('customer_id')
    
    if not customer_id:
        messages.warning(request, 'Vui lòng đăng nhập!')
        return redirect('login')
    
    data, status_code = ServiceClient.get_order_history(customer_id)
    
    orders = []
    if data.get('success'):
        orders = data.get('orders', [])
    
    return render(request, 'gateway/order_history.html', {
        'orders': orders
    })


def recommendations(request):
    """Book recommendations page"""
    customer_id = request.session.get('customer_id')
    
    data, status_code = ServiceClient.get_recommendations(customer_id)
    
    books = []
    if data.get('success'):
        books = data.get('books', [])
    
    return render(request, 'gateway/recommendations.html', {
        'books': books
    })


def add_stock(request):
    """Add book to inventory (staff)"""
    if not request.session.get('staff'):
        messages.warning(request, 'Vui lòng đăng nhập staff!')
        return redirect('staff_login')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        
        data, status_code = ServiceClient.add_book(title, author, price, stock_quantity)
        
        if data.get('success'):
            messages.success(request, 'Đã thêm sách mới!')
            return redirect('catalog')
        else:
            messages.error(request, data.get('message', 'Lỗi thêm sách!'))
    
    return render(request, 'gateway/add_stock.html')
