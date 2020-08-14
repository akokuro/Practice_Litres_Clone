from rest_framework import serializers
from .models import ReadedBook, WantedBook

class ReadedBookSerializer(serializers.ModelSerializer):
    """Создаёт новую запись блога"""
    class Meta:
        model = ReadedBook
        fields = ('id', 'user_id', 'book_id',)

class WantedBookSerializer(serializers.ModelSerializer):
    """Создаёт новую запись блога"""
    class Meta:
        model = WantedBook
        fields = ('id', 'user_id', 'book_id',)

