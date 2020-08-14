from django.shortcuts import render

from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated

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


def comment_save(content, user, book):
    comment = Comment(content=content, pub_date_time=datetime.now(), user_id=user, book_id=book)
    comment.save()

class  WriteCommentAPIView(APIView):
    """ Заполнение таблицы книг 
    Доступен всем пользователям"""
    permission_classes = [AllowAny]
    

    def post(self, request):
        """ Вносит данные в таблицу книг, если данная таблица пуста """
        if "" in request.query_params and request.query_params[""]:
            user = request.user
            book = Book.objects.filter(title=request.query_params[""])
            if(ReadedBook.objects.filter(user_id=user, book_id=book[0])):
                content = request.data.get("content")
                comment_save(content, user, book[0])
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response("Нельзя оставлять отзывы на непрочитанную книгу", status=status.HTTP_403_FORBIDDEN)

def similar(a, b):
    return distance(a, b)



class  GetLastSimilarBookCommentAPIView(APIView):
    """ Заполнение таблицы книг 
    Доступен всем пользователям"""
    permission_classes = [AllowAny]

    def get(self, request):
        """ Вносит данные в таблицу книг, если данная таблица пуста """
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