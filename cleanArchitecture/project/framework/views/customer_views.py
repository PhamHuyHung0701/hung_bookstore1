"""
Customer Views - Framework Layer (Django)
"""
from django.shortcuts import render, redirect
from django.contrib import messages

from project.interfaces.controllers.customer_controller import CustomerController


def register(request):
    """Đăng ký khách hàng mới"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        controller = CustomerController()
        result = controller.register(name, email, password, confirm_password)

        if result['success']:
            messages.success(request, result['message'])
            return redirect('customer:login')
        else:
            messages.error(request, result['message'])
            return render(request, 'customer/register.html')

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
        controller = CustomerController()
        result = controller.login(email, password)

        if result['success']:
            customer = result['customer']
            request.session['customer_id'] = customer.id
            request.session['customer_name'] = customer.name
            messages.success(request, result['message'])
            return redirect('book:catalog')
        else:
            messages.error(request, result['message'])

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

    controller = CustomerController()
    result = controller.get_profile(customer_id)

    if result['success']:
        return render(request, 'customer/profile.html', {'customer': result['customer']})
    
    messages.error(request, result.get('message', 'Có lỗi xảy ra'))
    return redirect('customer:login')


def staff_login(request):
    """Đăng nhập staff"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Simple check - hardcoded staff account
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
