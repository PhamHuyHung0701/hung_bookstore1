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
    """Customer login page"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
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
