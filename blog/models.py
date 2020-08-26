from django.db import models

# Create your models here.

from test_auth.models import MyUser
from datetime import datetime

class BlogManager(models.Manager):
    """Менеджер объектов класса Post"""
    def create(self, headline, author, content=None):
        """Создаёт запись блога и возвращает её"""
        if not headline:
            raise ValueError('Заголовок должно быть установлено')
        if not author:
            raise ValueError('Автор должен быть установлен')
        post = self.model(headline=headline, author=author, pub_date=datetime.now(), content=content)
        post.save(using=self._db)
        return post
        
    def read(self, author):
        """Находит все записи автора author и возвращает их"""
        if not author:
            raise ValueError('Автор должен быть установлен')
        posts = self.filter(author=author)
        return posts

    def update(self, Id, content):
        """Обновляет запись, id которой равен Id"""
        if not Id:
            raise ValueError('Id должен быть установлен')
        post = self.get(id=Id)
        if content:
            post.content = content
        post.save()
        return post
    
    def delete(self, Id):
        """Удаляет запись, id которой равен Id"""
        self.filter(id=Id).delete()



class Post(models.Model):
    """Модель записи блога"""
    headline = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content = models.TextField()
    
    # Сообщает Django, что класс BlogManager, определенный выше, 
    # должен управлять объектами этого типа.
    objects = BlogManager()

    def __str__(self):
        return self.headline