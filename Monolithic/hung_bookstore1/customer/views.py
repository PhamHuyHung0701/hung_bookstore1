from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer
from hung_bookstore1.book.models import Staff


def register(request):
    """Đăng ký khách hàng mới"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate
        if password != confirm_password:
            messages.error(request, 'Mật khẩu xác nhận không khớp!')
            return render(request, 'customer/register.html')

        # Check if email already exists
        if Customer.objects.filter(email=email).exists():
            messages.error(request, 'Email đã được sử dụng!')
            return render(request, 'customer/register.html')

        # Create new customer
        customer = Customer(name=name, email=email)
        customer.set_password(password)
        customer.save()

        messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
        return redirect('customer:login')

    return render(request, 'customer/register.html')


def login(request):
    """Đăng nhập - hỗ trợ cả Customer và Staff"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Kiểm tra xem có phải tài khoản staff không
        if email == 'staff@bookstore.com' and password == 'staff':
            request.session['staff'] = True
            request.session['staff_email'] = email
            messages.success(request, 'Đăng nhập staff thành công!')
            return redirect('book:add_stock')

        # Nếu không phải staff, kiểm tra customer
        try:
            customer = Customer.objects.get(email=email)
            if customer.check_password(password):
                # Lưu thông tin đăng nhập vào session
                request.session['customer_id'] = customer.id
                request.session['customer_name'] = customer.name
                messages.success(request, f'Chào mừng {customer.name}!')
                return redirect('book:catalog')
            else:
                messages.error(request, 'Mật khẩu không đúng!')
        except Customer.DoesNotExist:
            messages.error(request, 'Email không tồn tại!')

    return render(request, 'customer/login.html')


def logout(request):
    """Đăng xuất"""
    request.session.flush()
    messages.success(request, 'Đã đăng xuất thành công!')
    return redirect('customer:login')


def profile(request):
    """Xem thông tin cá nhân"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('customer:login')

    customer = Customer.objects.get(id=customer_id)
    return render(request, 'customer/profile.html', {'customer': customer})


def staff_login(request):
    """Đăng nhập staff"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Simple check
        if email == 'staff@bookstore.com' and password == 'staff':
            request.session['staff'] = True
            messages.success(request, 'Đăng nhập staff thành công!')
            return redirect('book:add_stock')
        else:
            messages.error(request, 'Thông tin đăng nhập không đúng!')
    
    return render(request, 'customer/staff_login.html')


def staff_logout(request):
    """Đăng xuất staff"""
    request.session.pop('staff', None)
    messages.success(request, 'Đã đăng xuất staff!')
    return redirect('book:catalog')
