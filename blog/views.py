from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
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

    def list(self, request, pk=None, **kwargs):
        authors = MyUser.objects.all()
        serializer = ViewUserSerializer(authors, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        author = MyUser.objects.get(id=pk)
        posts = Post.objects.read(author)
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None, **kwargs):
        Post.objects.delete(Id=pk)
        return Response(status=status.HTTP_200_OK)
