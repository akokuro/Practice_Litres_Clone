import re
import time
import requests
import threading
from bs4 import BeautifulSoup

from .models import Book

class Parser():

    site_adress = "https://www.goodreads.com"

    def __init__(self):
        self.books = []

    def get_urls(self):
        """Получает все ссылки со страницы с адресом url и возвращает их"""
        url = "https://www.goodreads.com/list/show/2681.Time_Magazine_s_All_Time_100_Novels"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        pattern = re.compile(r'\/book\/show\/.+')
        urls = []
        for url in soup.find_all("a", href=pattern):
            if url['href'] not in urls:
                urls.append(url['href'])
        return urls


    def parse_book(self, url):
        """Возвращает название, автора и описание книги из страницы с адресом url"""
        url = Parser.site_adress + url[1]
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        title = soup.find("meta",  property="og:title")["content"]
        author = soup.title.string.split(" by ")[1]
        description = soup.find("meta",  property="og:description")["content"]
        return title, author, description
        
    def save_book_in_bd(self, title, author, description):
        """Сохраняет книгу в бд"""
        Book.objects.create(title, author, description)

    def parse_books(self, urls):
        """Парсит переданные ссылки, 
        сохраняет полученное описание книги в бд"""
        for url in enumerate(urls):
            self.save_book_in_bd(*self.parse_book(url))


    def save_books_in_bd(self):
        """Получает ссылки на все книги,
        парсит данные с этих ссылок в несколько потоков, 
        сохраняет полученные книги в бд"""
        urls = self.get_urls()
        threads = list()
        size = len(urls)
        thread_count = 20
        for index in range(thread_count):
            start = size // thread_count * index
            stop = min(size // thread_count * (index + 1), size)
            thr = threading.Thread(target=self.parse_books, args=(urls[start:stop],))
            threads.append(thr)
            thr.start()
        for thr in threads:
            thr.join()