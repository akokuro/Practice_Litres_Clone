from django.db import models
from test_auth.models import MyUser
from catalog.models import Book

class CommentManager(models.Manager):
    def create(self, content, pub_date_time, user_id, book_id):
        if not content:
            raise ValueError('Пустые комментарии недопустимы')
        if not pub_date_time:
            raise ValueError('Дата и время должны быть установлены')
        if not user_id:
            raise ValueError('Пользователь должен быть установлен')
        if not book_id:
            raise ValueError('Книга должна быть установлена')
        comment = self.model(content=content, pub_date_time=pub_date_time, user_id=user_id, book_id=book_id)
        comment.save(using=self._db)
        return comment

    def delete(self, Id):
        self.filter(id=Id).delete()

class Comment(models.Model):
    content = models.CharField(max_length=4096)
    pub_date_time = models.DateTimeField()
    user_id = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)
    book_id = models.ForeignKey(to=Book, on_delete=models.CASCADE)

    # Сообщает Django, что класс BlogManager, определенный выше, 
    # должен управлять объектами этого типа.
    objects = CommentManager()