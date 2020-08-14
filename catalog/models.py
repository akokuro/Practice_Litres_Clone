from django.db import models
from test_auth.models import MyUser

class CatalogManager(models.Manager):
    def create(self, title, author, description=None):
        if not title:
            raise ValueError('Заголовок должно быть установлено')
        if not author:
            raise ValueError('Автор должен быть установлен')
        book = self.model(title=title, author=author, description=description)
        book.save(using=self._db)
        return book
        
    def read(self):
        books = self.all()
        return books
    
    def delete(self, Id):
        self.filter(id=Id).delete()



class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.CharField(max_length=4096)
    
    # Сообщает Django, что класс BlogManager, определенный выше, 
    # должен управлять объектами этого типа.
    objects = CatalogManager()

    def __str__(self):
        return self.title