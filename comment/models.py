from django.db import models
from test_auth.models import MyUser
from catalog.models import Book

from langdetect import detect
from datetime import datetime
from profanity_check import predict

class CommentManager(models.Manager):
    """Менеджер объектов класса Comment"""
    def create(self, content, user_id, book_id):
        "Создаёт новый комментарий"
        if not content:
            raise ValueError('Пустые комментарии недопустимы')
        if detect(content) != 'en':
            raise ValueError('Комментарий должен быть написан на английском языке')
        if predict([content])[0] == 1:
            raise ValueError('Нецензурная лексика недопустима')
        if not user_id:
            raise ValueError('Пользователь должен быть установлен')
        if not book_id:
            raise ValueError('Книга должна быть установлена')
        comment = self.model(content=content, pub_date_time=datetime.now(), user_id=user_id, book_id=book_id)
        comment.save(using=self._db)
        return comment

class Comment(models.Model):
    """Модель комментария"""
    content = models.CharField(max_length=4096)
    pub_date_time = models.DateTimeField()
    user_id = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)
    book_id = models.ForeignKey(to=Book, on_delete=models.CASCADE)

    # Сообщает Django, что класс BlogManager, определенный выше, 
    # должен управлять объектами этого типа.
    objects = CommentManager()