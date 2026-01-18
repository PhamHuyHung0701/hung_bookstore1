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
    """Đăng nhập"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

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
