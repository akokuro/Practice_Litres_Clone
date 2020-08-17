from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Book
from .serializers import CatalogSerializer
from .book_parser import Parser

from test_auth.models import MyUser
from test_auth.parsers import EverythingParser
from test_auth.backends import JWTAuthentication
from test_auth.serializers import ViewUserSerializer

from rest_framework import viewsets

class CatalogViewSet(viewsets.ModelViewSet):
    """Каталог книг"""
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]
    queryset = Book.objects.all()
    serializer_class = CatalogSerializer

    def get_permissions(self):
        """Настраивает доступ: get-запросы доступны любому, а остальные - только администратору"""
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request, **kwargs):
        """Возвращает список всех книг в каталоге"""
        books = Book.objects.read()
        serializer = self.serializer_class(books, many=True)
        return Response(serializer.data)

class FillDbAPIView(APIView):
    """ Заполнение таблицы книг 
    Доступен администратору"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        """ Вносит данные в таблицу книг, если данная таблица пуста"""
        if not len(Book.objects.read()) > 0:
            parser = Parser()
            parser.save_books_in_bd()
        return Response(status=status.HTTP_200_OK)
