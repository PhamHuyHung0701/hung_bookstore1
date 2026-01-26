"""
Book Views - Framework Layer (Django)
"""
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages

from project.interfaces.controllers.book_controller import BookController


def catalog(request):
    """Xem danh sách sách"""
    search_query = request.GET.get('search', '')
    
    controller = BookController()
    result = controller.get_catalog(search_query)

    return render(request, 'book/catalog.html', {
        'books': result['books'],
        'search_query': result['search_query']
    })


def book_detail(request, book_id):
    """Xem chi tiết sách"""
    controller = BookController()
    result = controller.get_detail(book_id)

    if result['success']:
        return render(request, 'book/detail.html', {'book': result['book']})
    
    raise Http404("Không tìm thấy sách")


def add_stock(request):
    """Nhân viên nhập sách vào kho"""
    if not request.session.get('staff'):
        messages.warning(request, 'Vui lòng đăng nhập staff!')
        return redirect('customer:staff_login')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        
        controller = BookController()
        result = controller.add_book(title, author, price, stock_quantity)
        
        if result['success']:
            messages.success(request, 'Sách đã được thêm vào kho!')
            return redirect('book:catalog')
        else:
            messages.error(request, f'Lỗi: {result["message"]}')
    
    return render(request, 'book/add_stock.html')


def recommendations(request):
    """Gợi ý sách dựa trên lịch sử mua"""
    customer_id = request.session.get('customer_id')
    if customer_id:
        controller = BookController()
        result = controller.get_recommendations(customer_id)
        recommended_books = result['books']
    else:
        recommended_books = []
    
    return render(request, 'book/recommendations.html', {
        'recommended_books': recommended_books
    })
