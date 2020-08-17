from django.shortcuts import render

from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated

from .serializers import CommentSerializer
from .models import Comment

from catalog.models import Book

from personal_catalog.models import ReadedBook

from test_auth.models import MyUser
from test_auth.parsers import EverythingParser
from test_auth.backends import JWTAuthentication
from test_auth.serializers import ViewUserSerializer

from datetime import datetime
from Levenshtein import distance


class  WriteCommentAPIView(APIView):
    """Создание нового комментария
    Доступен только авторизованому пользователю"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Создаёт новый комментарий
        Если книги с указанным в url названием не найдена, возвращает ошибку 404
        Если книга пользователем не прочитана, возвращает ошибку 403"""
        if "" in request.query_params and request.query_params[""]:
            user = request.user
            try:
                book = Book.objects.filter(title=request.query_params[""])
            except Exception:
                    return Response("Книга с таким названием не найдена", status=status.HTTP_404_NOT_FOUND)
            if(ReadedBook.objects.filter(user_id=user, book_id=book[0])):
                content = request.data.get("content")
                Comment.objects.create(content, user, book[0])
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response("Нельзя оставлять отзывы на непрочитанную книгу", status=status.HTTP_403_FORBIDDEN)

def similar(a, b):
    """Находит расстояние Левенштейна между строкой a и b"""
    return distance(a, b)


class  GetLastSimilarBookCommentAPIView(APIView):
    """ Заполнение таблицы книг 
    Доступен всем пользователям"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Возвращает три последних комментария на книгу с самым похожим названием на указанное в url"""
        if "" in request.query_params and request.query_params[""]:
            books = Book.objects.read()
            books = list(sorted(books, key=lambda b : similar(request.query_params[""], b.title)))
            comments = Comment.objects.filter(book_id=books[1])
            comments = list(
                sorted(
                    comments, 
                    key=lambda b: (b.pub_date_time.replace(tzinfo=None) - datetime(1970,1,1)).total_seconds(), 
                    reverse=True
                )
            )
            if len(comments) > 3:
                comments = comments[:3]
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)