from django.shortcuts import render, get_object_or_404
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
