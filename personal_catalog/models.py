from django.db import models
from test_auth.models import MyUser
from catalog.models import Book

class ReadedBookManager(models.Manager):
    """Менеджер объектов класса ReadedBook"""
    def create(self, user_id, book_id):
        if not user_id:
            raise ValueError('Пользователь должен быть установлен')
        if not book_id:
            raise ValueError('Книга должна быть установлена')
        book = self.model(user_id=user_id, book_id=book_id)
        book.save(using=self._db)
        return book
        
    def read(self):
        books = self.all()
        return books
    
    def delete(self, Id):
        self.filter(id=Id).delete()

class WantedBookManager(ReadedBookManager):
    """Менеджер объектов класса WantedBook"""
    pass

class ReadedBook(models.Model):
    """Модель прочитанной книги"""
    user_id = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)
    book_id = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    # Сообщает Django, что класс BlogManager, определенный выше, 
    # должен управлять объектами этого типа.
    objects = ReadedBookManager()

class WantedBook(models.Model):
    """Модель книги, которую пользователь хочет прочитать"""
    user_id = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)
    book_id = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    # Сообщает Django, что класс BlogManager, определенный выше, 
    # должен управлять объектами этого типа.
    objects = WantedBookManager()

