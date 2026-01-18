"""
API Gateway - Web Views for frontend
Calls microservices via REST APIs
"""
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from django.conf import settings


# Service URLs
CUSTOMER_API = 'http://localhost:8000/api/customers'
BOOK_API = 'http://localhost:8000/api/books'
CART_API = 'http://localhost:8000/api/cart'


def register(request):
    """Customer registration page"""
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'confirm_password': request.POST.get('confirm_password'),
        }
        
        try:
            response = requests.post(f'{CUSTOMER_API}/register/', json=data, timeout=5)
            result = response.json()
            
            if result.get('success'):
                messages.success(request, result.get('message', 'Đăng ký thành công!'))
                return redirect('gateway:login')
            else:
                error_msg = result.get('message') or str(result.get('errors', 'Có lỗi xảy ra'))
                messages.error(request, error_msg)
        except requests.RequestException as e:
            messages.error(request, f'Lỗi kết nối đến service: {str(e)}')

    return render(request, 'gateway/register.html')


def login(request):
    """Customer login page"""
    if request.method == 'POST':
        data = {
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
        }
        
        try:
            response = requests.post(f'{CUSTOMER_API}/login/', json=data, timeout=5)
            result = response.json()
            
            if result.get('success'):
                customer = result.get('customer')
                request.session['customer_id'] = customer['id']
                request.session['customer_name'] = customer['name']
                messages.success(request, result.get('message', 'Đăng nhập thành công!'))
                return redirect('gateway:catalog')
            else:
                messages.error(request, result.get('message', 'Đăng nhập thất bại!'))
        except requests.RequestException as e:
            messages.error(request, f'Lỗi kết nối đến service: {str(e)}')

    return render(request, 'gateway/login.html')


def logout(request):
    """Customer logout"""
    request.session.flush()
    messages.success(request, 'Đã đăng xuất thành công!')
    return redirect('gateway:login')


def profile(request):
    """Customer profile page"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('gateway:login')

    try:
        response = requests.get(f'{CUSTOMER_API}/{customer_id}/', timeout=5)
        result = response.json()
        
        if result.get('success'):
            return render(request, 'gateway/profile.html', {'customer': result['customer']})
        else:
            messages.error(request, 'Không tìm thấy thông tin khách hàng')
            return redirect('gateway:login')
    except requests.RequestException as e:
        messages.error(request, f'Lỗi kết nối đến service: {str(e)}')
        return redirect('gateway:login')


def catalog(request):
    """Book catalog page"""
    search_query = request.GET.get('search', '')
    
    try:
        params = {'search': search_query} if search_query else {}
        response = requests.get(f'{BOOK_API}/', params=params, timeout=5)
        result = response.json()
        
        books = result.get('books', [])
    except requests.RequestException:
        books = []
        messages.error(request, 'Không thể tải danh sách sách')

    return render(request, 'gateway/catalog.html', {
        'books': books,
        'search_query': search_query
    })


def book_detail(request, book_id):
    """Book detail page"""
    try:
        response = requests.get(f'{BOOK_API}/{book_id}/', timeout=5)
        result = response.json()
        
        if result.get('success'):
            return render(request, 'gateway/book_detail.html', {'book': result['book']})
        else:
            messages.error(request, 'Không tìm thấy sách')
            return redirect('gateway:catalog')
    except requests.RequestException:
        messages.error(request, 'Không thể tải thông tin sách')
        return redirect('gateway:catalog')


def view_cart(request):
    """View shopping cart"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.warning(request, 'Vui lòng đăng nhập để xem giỏ hàng!')
        return redirect('gateway:login')

    try:
        response = requests.get(f'{CART_API}/{customer_id}/', timeout=5)
        result = response.json()
        
        if result.get('success'):
            cart = result.get('cart', {})
            return render(request, 'gateway/cart.html', {
                'cart': cart,
                'cart_items': cart.get('items', [])
            })
    except requests.RequestException:
        messages.error(request, 'Không thể tải giỏ hàng')

    return render(request, 'gateway/cart.html', {'cart': None, 'cart_items': []})


def add_to_cart(request, book_id):
    """Add book to cart"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.warning(request, 'Vui lòng đăng nhập để thêm vào giỏ hàng!')
        return redirect('gateway:login')

    try:
        response = requests.post(
            f'{CART_API}/{customer_id}/add/',
            json={'book_id': book_id, 'quantity': 1},
            timeout=5
        )
        result = response.json()
        
        if result.get('success'):
            messages.success(request, result.get('message', 'Đã thêm vào giỏ hàng!'))
        else:
            messages.error(request, result.get('message', 'Không thể thêm vào giỏ hàng!'))
    except requests.RequestException:
        messages.error(request, 'Lỗi kết nối đến service')

    return redirect('gateway:catalog')


def update_cart_item(request, item_id):
    """Update cart item quantity"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('gateway:login')

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            response = requests.put(
                f'{CART_API}/{customer_id}/items/{item_id}/',
                json={'quantity': quantity},
                timeout=5
            )
            result = response.json()
            
            if result.get('success'):
                messages.success(request, result.get('message', 'Đã cập nhật!'))
            else:
                messages.error(request, result.get('message', 'Không thể cập nhật!'))
        except requests.RequestException:
            messages.error(request, 'Lỗi kết nối đến service')

    return redirect('gateway:cart')


def remove_from_cart(request, item_id):
    """Remove item from cart"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('gateway:login')

    try:
        response = requests.delete(
            f'{CART_API}/{customer_id}/items/{item_id}/remove/',
            timeout=5
        )
        result = response.json()
        
        if result.get('success'):
            messages.success(request, result.get('message', 'Đã xóa khỏi giỏ hàng!'))
        else:
            messages.error(request, result.get('message', 'Không thể xóa!'))
    except requests.RequestException:
        messages.error(request, 'Lỗi kết nối đến service')

    return redirect('gateway:cart')
