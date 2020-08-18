from rest_framework.test import APITestCase as TestCase
from rest_framework.test import APIClient
from django.core.exceptions import ValidationError
from django.urls import reverse

from catalog.models import Book

from .models import ReadedBook, WantedBook

from test_auth.models import MyUser as User
from test_auth.serializers import RegistrationSerializer


class BlogListViewTest(TestCase):
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
        _user = User.objects.filter(username=name)[0]
        number_of_book = 5
        books = []
        for book_num in range(number_of_book):
            title = str(book_num) + " book"
            author = str(book_num) + " author"
            description = str(book_num) + " description"
            books.append(Book.objects.create(title, author, description))
        WantedBook.objects.create(_user, books[0])
        ReadedBook.objects.create(_user,books[1])
     
    def test_add_wantedbook_authorize(self):
        """Тестирование обращения по адресу add
        добавление книги в желаемые авторизованным пользователем"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get('/add?=2 book')
        self.assertEqual(resp.status_code, 201)

    def test_add_wantedbook_unauthorize(self):
        """Тестирование обращения по адресу add
        добавление книги в желаемые неавторизованным пользователем"""
        resp = self.client.get('/add?=2 book')
        self.assertEqual(resp.status_code, 401)

    def test_add_readedbook_authorize(self):
        """Тестирование обращения по адресу add
        добавление книги в прочитанные авторизованным пользователем"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get('/add?=3 book&read=true')
        self.assertEqual(resp.status_code, 201)

    def test_add_readedbook_unauthorize(self):
        """Тестирование обращения по адресу add
        добавление книги в прочитанные неавторизованным пользователем"""
        resp = self.client.get('/add?=3 book&read=true')
        self.assertEqual(resp.status_code, 401)    

    def test_add_book_without_name_in_url(self):
        """Тестирование обращения по адресу add без указания названия книги авторизованным пользователем"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get('/add')
        self.assertEqual(resp.status_code, 404)
    
    def test_add_book_with_incorrect_name(self):
        """Тестирование обращения по адресу add с указанием несуществующего названия книги авторизованным пользователем"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get('/add?=33 book')
        self.assertEqual(resp.status_code, 404)    

    def test_delete_wantedbook(self):
        """Тестирование обращения по адресу delete 
        удаление книги из желаемых авторизованным пользователем"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get('/delete?=0 book')
        self.assertEqual(resp.status_code, 200)

    def test_delete_readedbook(self):
        """Тестирование обращения по адресу delete 
        удаление книги из прочитанных авторизованным пользователем"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get('/delete?=1 book&read=true')
        self.assertEqual(resp.status_code, 200)

    def test_delete_book_without_name_in_url(self):
        """Тестирование обращения по адресу delete без указания имени книги в url авторизованным пользователем"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get('/delete')
        self.assertEqual(resp.status_code, 404)
    
    def test_delete_book_with_incorrect_name(self):
        """Тестирование обращения по адресу delete с несуществующим названием книги авторизованным пользователем"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get('/delete?=33 book')
        self.assertEqual(resp.status_code, 404)

    def test_get_readed_book_authorize(self):
        """Тестирование обращения по адресу add
        получения списка прочитанных книг авторизованным пользователем"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get('/stat?read=true')
        self.assertEqual(resp.status_code, 200)

    def test_get_readed_book_unauthorize(self):
        """Тестирование обращения по адресу add
        получения списка прочитанных книг неавторизованным пользователем"""
        resp = self.client.get('/stat?read=true')
        self.assertEqual(resp.status_code, 401)

    def test_get_wanted_book_authorize(self):
        """Тестирование обращения по адресу add
        получения списка желаемых книг авторизованным пользователем"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get('/stat')
        self.assertEqual(resp.status_code, 200)

    def test_get_wanted_book_unauthorize(self):
        """Тестирование обращения по адресу add
        получения списка желаемых книг неавторизованным пользователем"""
        resp = self.client.get('/stat')
        self.assertEqual(resp.status_code, 401)
        