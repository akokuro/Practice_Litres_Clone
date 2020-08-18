from rest_framework.test import APITestCase as TestCase
from rest_framework.test import APIClient
from django.core.exceptions import ValidationError
from django.urls import reverse

from .models import Post

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
        number_of_blog = 5
        for post_num in range(number_of_blog):
            headline = str(post_num) + " post"
            author = User.objects.filter(username=name)[0]
            content = str(post_num) + " content"
            Post.objects.create(headline, author, content)
     
    def test_write_authorize(self):
        """Тестирование обращения по адресу write с целью создания нового поста авторизованным пользователем"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.post('/write/', data={"headline":"BLOG", "content":"FIRST"})
        self.assertEqual(resp.status_code, 201)

    def test_write_unauthorize(self):
        """Тестирование обращения по адресу write с целью создания нового поста неавторизованным пользователем"""
        resp = self.client.post('/write/', data={"headline":"BLOG", "content":"FIRST"})
        self.assertEqual(resp.status_code, 401)

    def test_list_authorize(self):
        """Тестирование обращения по адресу write без указания pk авторизованным пользователем"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get('/write/')
        self.assertEqual(resp.status_code, 200)

    def test_list_unauthorize(self):
        """Тестирование обращения по адресу write без указания pk неавторизованным пользователем"""
        resp = self.client.get('/write/1/')
        self.assertEqual(resp.status_code, 401)

    
    def test_get_authorize(self):
        """Тестирование обращения по адресу write с передованием pk"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get('/write/1/')
        self.assertEqual(resp.status_code, 200)

    def test_get_unauthorize(self):
        """Тестирование обращения по адресу write с передованием pk неавторизованным пользователем"""
        resp = self.client.get('/write/1/')
        self.assertEqual(resp.status_code, 401)
