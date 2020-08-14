from django.db import models

# Create your models here.

from test_auth.models import MyUser

class BlogManager(models.Manager):
    def create(self, headline, author, pub_date=None, content=None):
        if not headline:
            raise ValueError('Заголовок должно быть установлено')
        if not author:
            raise ValueError('Автор должен быть установлен')
        post = self.model(headline=headline, author=author, pub_date=pub_date, content=content)
        post.save(using=self._db)
        return post
        
    def read(self, author):
        if not author:
            raise ValueError('Автор должен быть установлен')
        posts = self.filter(author=author)
        return posts

    def update(self, Id, content):
        if not Id:
            raise ValueError('Id должен быть установлен')
        post = self.get(id=Id)
        if content:
            post.content = content
        post.save()
        return post
    
    def delete(self, Id):
        self.filter(id=Id).delete()



class Post(models.Model):
    headline = models.CharField(max_length=255)
    pub_date = models.DateField()
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=4096)
    
    # Сообщает Django, что класс BlogManager, определенный выше, 
    # должен управлять объектами этого типа.
    objects = BlogManager()

    def __str__(self):
        return self.headline