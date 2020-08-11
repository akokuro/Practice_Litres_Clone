from rest_framework import serializers
from .models import Post
class BlogPostSerializer(serializers.ModelSerializer):
    """Создаёт новую запись блога"""
    class Meta:
        model = Post
        fields = ('headline', 'pub_date', 'author', 'content',)
