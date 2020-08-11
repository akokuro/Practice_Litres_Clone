from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Post
from .serializers import BlogPostSerializer
from test_auth.parsers import EverythingParser
from test_auth.backends import JWTAuthentication

from rest_framework import viewsets

class BlogViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Post.objects.all()
    serializer_class = BlogPostSerializer


    def update(self, request, pk=None):
        print(pk, request)


    def destroy(self, *args, **kwargs):
        print("destroy", args, kwargs)

# class BlogApiView(APIView):
#     """Блог пользователя
#     Доступен только авторизованным пользователям"""
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     parser_classes = [EverythingParser]
#     def post(self, request):
#         """Обработка post-запроса
#         Если пользователь авторизован, то возвращает тело запроса"""
#         post = Post.objects.create()
#         return Response(request.data, status=status.HTTP_200_OK)
