from django.shortcuts import render

from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import ReadedBookSerializer, WantedBookSerializer

from .models import ReadedBook, WantedBook

from catalog.models import Book

from test_auth.models import MyUser
from test_auth.parsers import EverythingParser
from test_auth.backends import JWTAuthentication
from test_auth.serializers import ViewUserSerializer

def create_readed_book(user, book):
    readed_book = ReadedBook.objects.create(user, book)
    readed_book.save()

def create_wanted_book(user, book):
    readed_book = WantedBook.objects.create(user, book)
    readed_book.save()

class  AddInPersonalCatalogAPIView(APIView):
    """ Заполнение таблицы книг 
    Доступен всем пользователям"""
    permission_classes = [AllowAny]

    def get(self, request):
        """ Вносит данные в таблицу книг, если данная таблица пуста """
        if "" in request.query_params and request.query_params[""]:
            if "read" in request.query_params and request.query_params["read"] == "true":
                try:
                    user = request.user
                    book = Book.objects.filter(title=request.query_params[""])
                    if not ReadedBook.objects.filter(user_id=user, book_id=book[0]):
                        create_readed_book(user, book[0])
                    return Response(status=status.HTTP_201_CREATED)
                except Exception:
                    return Response("Книга с таким названием не найдена", status=status.HTTP_404_NOT_FOUND)
            else:
                try:
                    user = request.user
                    book = Book.objects.filter(title=request.query_params[""])
                    if not WantedBook.objects.filter(user_id=user, book_id=book[0]):
                        create_wanted_book(user, book[0])
                    return Response(status=status.HTTP_201_CREATED)
                except Exception:
                    return Response("Книга с таким названием не найдена", status=status.HTTP_404_NOT_FOUND)


class  DeleteFromPersonalCatalogAPIView(APIView):
    """ Заполнение таблицы книг 
    Доступен всем пользователям"""
    permission_classes = [AllowAny]

    def get(self, request):
        """ Вносит данные в таблицу книг, если данная таблица пуста """
        if "" in request.query_params and request.query_params[""]:
            if "read" in request.query_params and request.query_params["read"] == "true":
                try:
                    user = request.user
                    book = Book.objects.filter(title=request.query_params[""])
                    ReadedBook.objects.filter(user_id=user, book_id=book[0]).delete()
                    return Response(status=status.HTTP_200_OK)
                except Exception:
                    return Response("Прочитанная книга с таким названием не найдена", status=status.HTTP_404_NOT_FOUND)
            else:
                try:
                    user = request.user
                    book = Book.objects.filter(title=request.query_params[""])
                    WantedBook.objects.filter(user_id=user, book_id=book[0]).delete()
                    return Response(status=status.HTTP_200_OK)
                except Exception:
                    return Response("Книга с таким названием в желаемых не найдена", status=status.HTTP_404_NOT_FOUND)

class  PersonalCatalogAPIView(APIView):
    """ Заполнение таблицы книг 
    Доступен всем пользователям"""
    permission_classes = [AllowAny]

    def get(self, request):
        """ Вносит данные в таблицу книг, если данная таблица пуста """
        if "read" in request.query_params and request.query_params["read"] == "true":
            user = request.user
            books = ReadedBook.objects.filter(user_id=user)
            serializer = ReadedBookSerializer(books, many=True)
            return Response(serializer.data)
        else:
            user = request.user
            books = WantedBook.objects.filter(user_id=user)
            serializer = WantedBookSerializer(books, many=True)
            return Response(serializer.data)