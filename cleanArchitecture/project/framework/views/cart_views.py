"""
Cart Views - Framework Layer (Django)
"""
from django.shortcuts import render, redirect
from django.contrib import messages

from project.interfaces.controllers.cart_controller import CartController


def view_cart(request):
    """Xem giỏ hàng"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.warning(request, 'Vui lòng đăng nhập để xem giỏ hàng!')
        return redirect('customer:login')

    controller = CartController()
    result = controller.get_cart(customer_id)

    return render(request, 'cart/view_cart.html', {
        'cart': result['cart'],
        'cart_items': result['cart_items']
    })


def add_to_cart(request, book_id):
    """Thêm sách vào giỏ hàng"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.warning(request, 'Vui lòng đăng nhập để thêm vào giỏ hàng!')
        return redirect('customer:login')

    controller = CartController()
    result = controller.add_to_cart(customer_id, book_id)

    if result['success']:
        messages.success(request, result['message'])
    else:
        messages.error(request, result['message'])

    return redirect('book:catalog')


def update_cart_item(request, item_id):
    """Cập nhật số lượng sách trong giỏ hàng"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('customer:login')

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        controller = CartController()
        result = controller.update_cart_item(customer_id, item_id, quantity)

        if result['success']:
            messages.success(request, result['message'])
        else:
            messages.error(request, result['message'])

    return redirect('cart:view_cart')


def remove_from_cart(request, item_id):
    """Xóa sách khỏi giỏ hàng"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('customer:login')

    controller = CartController()
    result = controller.remove_from_cart(customer_id, item_id)

    if result['success']:
        messages.success(request, result['message'])
    else:
        messages.error(request, result['message'])

    return redirect('cart:view_cart')
