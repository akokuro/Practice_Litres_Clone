from rest_framework import serializers
from .models import ReadedBook, WantedBook

class ReadedBookSerializer(serializers.ModelSerializer):
    """Сериализатор прочитанной книги"""
    class Meta:
        model = ReadedBook
        fields = ('id', 'user_id', 'book_id',)

class WantedBookSerializer(serializers.ModelSerializer):
    """Сериализатор книги, которую пользователь хочет прочитать"""
    class Meta:
        model = WantedBook
        fields = ('id', 'user_id', 'book_id',)

