from rest_framework.test import APITestCase as TestCase

# Create your tests here.

from django.core.exceptions import ValidationError

from .serializers import RegistrationSerializer
from pymysql.err import IntegrityError
from .models import MyUser as User
from http.cookies import SimpleCookie
from django.urls import reverse

import json

class UserListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Настройка контекста для теста"""
        number_of_users = 5
        for author_num in range(number_of_users):
            name = 'Username%s' % author_num
            password = 'password%s' % author_num
            user = {"username":name, "password":password}
            serializer = RegistrationSerializer(data=user)
            serializer.is_valid(raise_exception=True)
            serializer.save()

    def signup(self, name, password):
        """Регистрация пользователя с именем name и паролем password"""
        resp = self.client.post('/signup/', data={'username': name, 'password': password}) 
        return resp

    def login(self, name, password):
        """Авторизация пользователя с именем name и паролем password"""
        resp = self.client.post('/login/', data={'username': name, 'password': password}) 
        return resp
        
    def test_unouthorithe_hello(self):
        """Тестирование обращения по адресу hello не авторизованным пользователем"""
        resp = self.client.post('/hello/')
        self.assertEqual(resp.status_code, 401)

    def test_authorize_hello(self):
        """Тестирование обращения по адресу hello с возвратом данных авторизованным пользователем"""
        resp = self.login('Username3', 'password3')
        json_data = json.decoder.JSONDecoder().decode(resp.content.decode("utf-8"))
        token = json_data["token"]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        resp = self.client.post('/hello/', data="adsgfsgfs", content_type="text/plain")
        self.assertEqual(resp.content, b'\"adsgfsgfs\"')
    
    def test_correct_signup(self):
        """Тестирование регистрации пользователя с корректными данными"""
        resp = self.signup('Username6', 'password6')
        self.assertEqual(resp.status_code, 201)

    def test_correct_login(self):
        """Тестирование авторизации пользователя с корректными данными"""
        resp = self.login('Username4', 'password4')
        self.assertEqual(resp.status_code, 200)

    def test_incorrect_login(self):
        """Тестирование автризации несуществущего пользователя"""
        resp = self.login('Username7', 'password6')
        self.assertEqual(resp.status_code, 401)

    def test_signup_with_exists_username(self):
        """Тестирование регистрации существующего пользователя"""
        resp = self.signup('Username4', 'password6')
        self.assertEqual(resp.status_code, 403)

    def test_signup_with_incorrect_credentials(self):
        """Тестирование регистрации пользователя с несоответствующими шаблону данными"""
        self.client.raise_request_exception = True
        # Логин больше 12 символов
        resp = self.signup('Username412313432113', 'password6')
        self.assertEqual(resp.status_code, 401)
        # Пароль больше 12 символов
        resp = self.signup('Username7', 'password63875389310')
        self.assertEqual(resp.status_code, 401)
        # Логин меньше 6 символов
        resp = self.signup('User', 'password6')
        self.assertEqual(resp.status_code, 401)
        # Пароль меньше 6 символов
        resp = self.signup('Username41', 'pass')
        self.assertEqual(resp.status_code, 401)
        # Логин состоит не только из английских букв и цифр
        resp = self.signup('Username4!', 'password6')
        self.assertEqual(resp.status_code, 401)
        # Пароль состоит не только из английский букв и цифр
        resp = self.signup('Username10', 'password!')
        self.assertEqual(resp.status_code, 401)
            
    def test_signup_authogenerate_credentials(self):
        """Тестирование регистрации автосгенерированного пользователя"""
        resp = self.client.post('/signup/?thinkforme=true') 
        self.assertEqual(resp.status_code, 201)

    
