from rest_framework import serializers
from .models import Post
class BlogPostSerializer(serializers.ModelSerializer):
    """Сериализатор записи блога"""
    class Meta:
        model = Post
        fields = ('id', 'headline', 'pub_date', 'author', 'content',)
