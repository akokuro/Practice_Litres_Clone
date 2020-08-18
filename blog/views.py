from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Post
from .serializers import BlogPostSerializer

from test_auth.models import MyUser
from test_auth.parsers import EverythingParser
from test_auth.backends import JWTAuthentication
from test_auth.serializers import ViewUserSerializer

from rest_framework import viewsets

class BlogViewSet(viewsets.ModelViewSet):
    """Блог пользователя
    Доступен только авторизованным пользователям"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    queryset = Post.objects.all()
    serializer_class = BlogPostSerializer

    def create(self, request, pk=None, **kwargs):
        """Создаёт новый пост
        Возвращает статус 201"""
        user = request.user
        headline = request.data.get("headline")
        content = request.data.get("content")
        Post.objects.create(headline, user, content)
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request, pk=None, **kwargs):
        """Возвращает список id и username существующих пользователей"""
        authors = MyUser.objects.all()
        serializer = ViewUserSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, **kwargs):
        """Возвращает все записи пользователя с id равным pk"""
        author = MyUser.objects.get(id=pk)
        posts = Post.objects.read(author)
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, **kwargs):
        """Удаляет запись с id равной pk"""
        Post.objects.delete(Id=pk)
        return Response(status=status.HTTP_200_OK)