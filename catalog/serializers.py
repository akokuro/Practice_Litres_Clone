from rest_framework import serializers
from .models import Book
class CatalogSerializer(serializers.ModelSerializer):
    """Сериализатор книги"""
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description',)
