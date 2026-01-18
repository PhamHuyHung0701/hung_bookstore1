from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem
from hung_bookstore1.book.models import Book
from hung_bookstore1.customer.models import Customer


def get_or_create_cart(request):
    """Lấy hoặc tạo giỏ hàng cho customer"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return None

    customer = Customer.objects.get(id=customer_id)
    cart, created = Cart.objects.get_or_create(customer=customer)
    return cart


def view_cart(request):
    """Xem giỏ hàng"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.warning(request, 'Vui lòng đăng nhập để xem giỏ hàng!')
        return redirect('customer:login')

    cart = get_or_create_cart(request)
    cart_items = cart.cartitem_set.all() if cart else []

    return render(request, 'cart/view_cart.html', {
        'cart': cart,
        'cart_items': cart_items
    })


def add_to_cart(request, book_id):
    """Thêm sách vào giỏ hàng"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.warning(request, 'Vui lòng đăng nhập để thêm vào giỏ hàng!')
        return redirect('customer:login')

    book = get_object_or_404(Book, id=book_id)
    cart = get_or_create_cart(request)

    if book.stock <= 0:
        messages.error(request, 'Sách đã hết hàng!')
        return redirect('book:catalog')

    # Kiểm tra xem sách đã có trong giỏ hàng chưa
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={'quantity': 1}
    )

    if not created:
        # Nếu đã có, tăng số lượng
        if cart_item.quantity < book.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'Đã thêm "{book.title}" vào giỏ hàng!')
        else:
            messages.warning(request, 'Không thể thêm nhiều hơn số lượng trong kho!')
    else:
        messages.success(request, f'Đã thêm "{book.title}" vào giỏ hàng!')

    return redirect('book:catalog')


def update_cart_item(request, item_id):
    """Cập nhật số lượng sách trong giỏ hàng"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('customer:login')

    cart_item = get_object_or_404(CartItem, id=item_id)

    # Kiểm tra quyền sở hữu
    if cart_item.cart.customer.id != customer_id:
        messages.error(request, 'Bạn không có quyền thực hiện thao tác này!')
        return redirect('cart:view_cart')

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0 and quantity <= cart_item.book.stock:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Đã cập nhật số lượng!')
        elif quantity <= 0:
            cart_item.delete()
            messages.success(request, 'Đã xóa sách khỏi giỏ hàng!')
        else:
            messages.error(request, 'Số lượng không hợp lệ!')

    return redirect('cart:view_cart')


def remove_from_cart(request, item_id):
    """Xóa sách khỏi giỏ hàng"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('customer:login')

    cart_item = get_object_or_404(CartItem, id=item_id)

    # Kiểm tra quyền sở hữu
    if cart_item.cart.customer.id != customer_id:
        messages.error(request, 'Bạn không có quyền thực hiện thao tác này!')
        return redirect('cart:view_cart')

    book_title = cart_item.book.title
    cart_item.delete()
    messages.success(request, f'Đã xóa "{book_title}" khỏi giỏ hàng!')

    return redirect('cart:view_cart')
