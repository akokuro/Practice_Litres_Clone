from rest_framework.test import APITestCase as TestCase
from rest_framework.test import APIClient
from django.core.exceptions import ValidationError
from django.urls import reverse

from .models import Book

from test_auth.models import MyUser as User
from test_auth.serializers import RegistrationSerializer

class CatalogListViewTest(TestCase):
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
        number_of_book = 5
        for book_num in range(number_of_book):
            title = str(book_num) + " book"
            author = str(book_num) + " author"
            description = str(book_num) + " description"
            Book.objects.create(title, author, description)
     
    def test_list_authorize(self):
        """Тестирование обращения по адресу catalog авторизованным пользователем для получения списка всех книг"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get('/catalog/')
        self.assertEqual(resp.status_code, 200)

    def test_list_unauthorize(self):
        """Тестирование обращения по адресу catalog неавторизованным пользователем для получения списка всех книг"""
        resp = self.client.get('/catalog/')
        self.assertEqual(resp.status_code, 200)

    def test_delete_book_authorize_user(self):
        """Тестирование обращения по адресу catalog с целью удаления книги авторизованным пользователем"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.delete('/catalog/1/')
        self.assertEqual(resp.status_code, 403)
    
    def test_delete_book_user_unauthorize(self):
        """Тестирование обращения по адресу catalog с целью удаления книги неавторизованным пользователем"""
        resp = self.client.delete('/catalog/1/')
        self.assertEqual(resp.status_code, 401)