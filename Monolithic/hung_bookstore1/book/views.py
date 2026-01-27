from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Book


def catalog(request):
    """Xem danh sách sách"""
    books = Book.objects.all()

    # Tìm kiếm theo title hoặc author
    search_query = request.GET.get('search', '')
    if search_query:
        books = books.filter(title__icontains=search_query) | books.filter(author__icontains=search_query)

    return render(request, 'book/catalog.html', {
        'books': books,
        'search_query': search_query
    })


def book_detail(request, book_id):
    """Xem chi tiết sách"""
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book/detail.html', {'book': book})


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
        
        Book.objects.create(
            title=title,
            author=author,
            price=price,
            stock_quantity=stock_quantity
        )
        messages.success(request, 'Sách đã được thêm vào kho!')
        return redirect('book:catalog')
    
    return render(request, 'book/add_stock.html')


def recommendations(request):
    """Gợi ý sách dựa trên lịch sử mua"""
    customer_id = request.session.get('customer_id')
    if customer_id:
        recommended_books = Book.recommend_for_customer(customer_id)
    else:
        recommended_books = Book.objects.filter(stock_quantity__gt=0).order_by('-stock_quantity')[:5]
    
    return render(request, 'book/recommendations.html', {
        'recommended_books': recommended_books
    })
