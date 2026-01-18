"""
Book Service Serializers
"""
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'stock', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class BookStockUpdateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
