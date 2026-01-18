"""
Book Views - Framework Layer (Django)
"""
from django.shortcuts import render
from django.http import Http404

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
