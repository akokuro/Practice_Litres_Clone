from django.shortcuts import render

from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated

from .serializers import ReadedBookSerializer, WantedBookSerializer

from .models import ReadedBook, WantedBook

from catalog.models import Book

from test_auth.models import MyUser
from test_auth.parsers import EverythingParser
from test_auth.backends import JWTAuthentication
from test_auth.serializers import ViewUserSerializer

def add_book_in_personal_catalog(request, manager):
    """Добавляет книгу, используя переданный manager, если её ещё нет у пользователя"""
    user = request.user
    book = Book.objects.filter(title=request.query_params[""])
    if not manager.filter(user_id=user, book_id=book[0]):
        manager.create(user, book[0])

class  AddInPersonalCatalogAPIView(APIView):
    """Добавление книги в персональный каталог
    Доступен только авторизованным пользователям"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Добавляет книгу с названием, указанным в url, в список прочитанных, если параметр read равен true и возвращает статус 201,
        иначе добавляет в список желаемых и возвращает статус 201
        Если книга с указанным в url названием не найдена в бд, то возвращает ошибку 404"""
        if "" in request.query_params and request.query_params[""]:
            try:
                if "read" in request.query_params and request.query_params["read"] == "true":
                    add_book_in_personal_catalog(request, ReadedBook.objects)
                else:
                    add_book_in_personal_catalog(request, WantedBook.objects)
                return Response(status=status.HTTP_201_CREATED)
            except Exception:
                return Response("Книга с таким названием не найдена", status=status.HTTP_404_NOT_FOUND)


def delete_book(request, manager):
    """Удаляет книгу с помощью менеджера manager"""
    user = request.user
    book = Book.objects.filter(title=request.query_params[""])
    manager.filter(user_id=user, book_id=book[0]).delete()

class  DeleteFromPersonalCatalogAPIView(APIView):
    """Удаление книги из персонального каталога
    Доступен только авторизованным пользователям"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Удаляет книгу с названием, указанным в url, из списка прочитанных, если параметр read равен true и возвращает статус 200,
        иначе удаляет из списка желаемых и возвращает статус 200
        Если книга с указанным в url названием не найдена в бд, то возвращает ошибку 404"""
        if "" in request.query_params and request.query_params[""]:
            try:
                if "read" in request.query_params and request.query_params["read"] == "true":
                    delete_book(request, ReadedBook.objects)
                else:
                    delete_book(request, WantedBook.objects)
                return Response(status=status.HTTP_200_OK)
            except Exception:
                return Response("Прочитанная книга с таким названием не найдена", status=status.HTTP_404_NOT_FOUND)

def get_book(request, manager, serializer):
    """Получает книги при попощи менедждера manager и сериализует их с помощью serializer """
    user = request.user
    books = manager.filter(user_id=user)
    return serializer(books, many=True)

class  PersonalCatalogAPIView(APIView):
    """Представление персонального каталога"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Возвращает список прочитанных пользователем книг, если параметр read равен true, иначе возвращает список желаемых"""
        if "read" in request.query_params and request.query_params["read"] == "true":
            serializer = get_book(request, ReadedBook.objects, ReadedBookSerializer)
        else:
            serializer = get_book(request, WantedBook.objects, WantedBookSerializer)
        return Response(serializer.data)