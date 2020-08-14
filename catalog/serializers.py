from rest_framework import serializers
from .models import Book
class CatalogSerializer(serializers.ModelSerializer):
    """Создаёт новую запись блога"""
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description',)
