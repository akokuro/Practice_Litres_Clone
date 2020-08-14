from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    """Создаёт новую запись блога"""
    class Meta:
        model = Comment
        fields = ('id', 'content', 'pub_date_time', 'user_id', 'book_id',)
