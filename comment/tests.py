from rest_framework.test import APITestCase as TestCase
from rest_framework.test import APIClient
from django.core.exceptions import ValidationError
from django.urls import reverse

from .models import Comment

from catalog.models import Book

from personal_catalog.models import ReadedBook

from test_auth.models import MyUser as User
from test_auth.serializers import RegistrationSerializer

class CommentListViewTest(TestCase):
    token = None
    @classmethod
    def setUpTestData(cls):
        """Настройка контекста для теста"""
        name = 'TestUser'
        password = 'password' 
        user = {"username":name, "password":password}
        serializer = RegistrationSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        cls.token = serializer.save().token
        cls.client = APIClient()
        titles = ["Loving", "Lolita", "Ganz"]
        number_of_book = 3
        books = []
        for book_num in range(number_of_book):
            title = titles[book_num]
            author = str(book_num) + " author"
            description = str(book_num) + " description"
            books.append(Book.objects.create(title, author, description))
        number_of_comment = 5
        ReadedBook.objects.create(User.objects.filter(username=name)[0], books[0])
        for comment_num in range(number_of_comment):
            content = "It's imposible! " + str(comment_num)
            author = User.objects.filter(username=name)[0]
            book = books[comment_num % 3]
            Comment.objects.create(content, author, book)
     
    def test_write_comment_on_url_without_bookname(self):
        """Тестирование обращения по адресу comment без указания названия книги в url"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.post('/comment/', data={"content":"It's great book!"})
        self.assertEqual(resp.status_code, 404)
    
    def test_write_comment_authorize_not_read_book(self):
        """Тестирование обращения по адресу comment 
        создание нового комментария авторизованным пользователем на непрочитанную книгу"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.post('/comment?=Lolita', data={"content":"It's great book!"})
        self.assertEqual(resp.status_code, 403)

    def test_write_comment_authorize_read_book(self):
        """Тестирование обращения по адресу comment
        создание нового комментария авторизованным пользователем на прочитанную книгу"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.post('/comment?=Loving', data={"content":"It's great book!"})
        self.assertEqual(resp.status_code, 201)

    def test_write_comment_unauthorize(self):
        """Тестирование обращения по адресу comment неавторизованным пользователем"""
        resp = self.client.post('/comment?=Loving', data={"content":"It's great book!"})
        self.assertEqual(resp.status_code, 401)

    def test_write_comment_with_obscene(self):
        """Тестирование обращения по адресу comment
        создание нового комментария с ненормативной лексикой авторизованным пользователем на прочитанную книгу"""
        self.client.raise_request_exception = True
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.post('/comment?=Loving', data={"content":"What a fucking sweet t-shirt you have there!"})
        self.assertEqual(resp.status_code, 403)

    def test_write_comment_not_on_english(self):
        """Тестирование обращения по адресу comment
        создание нового комментария с ненормативной лексикой авторизованным пользователем на прочитанную книгу"""
        self.client.raise_request_exception = True
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.post('/comment?=Loving', data={"content":"Какая чудесная книга!"})
        self.assertEqual(resp.status_code, 403)

    def test_get_comments_with_book_in_url(self):
        """Тестирование обращения по адресу comment
        получение трёх комментариев по книге с самым похожим названием на указанное в url"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get('/reviews?=Lolita')
        self.assertEqual(resp.status_code, 200)

    def test_get_comments_without_book_in_url(self):
        """Тестирование обращения по адресу comment
        получение трёх комментариев по книге с самым похожим названием на указанное в url"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get('/reviews')
        self.assertEqual(resp.status_code, 404)