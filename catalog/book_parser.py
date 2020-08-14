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
        url = "https://www.goodreads.com/list/show/2681.Time_Magazine_s_All_Time_100_Novels"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        pattern = re.compile(r'\/book\/show\/.+')
        urls = []
        for url in soup.find_all("a", href=pattern):
            if url['href'] not in urls:
                urls.append(url['href'])
        return urls


    def get_book(self, url):
        url = Parser.site_adress + url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        title = soup.find("meta",  property="og:title")["content"]
        author = soup.title.string.split(" by ")[1]
        description = soup.find("meta",  property="og:description")["content"]
        book = Book.objects.create(title, author, description)
        book.save()
        return book
    
    def get_books(self, urls):
        for i, url in enumerate(urls):
            self.books.append(self.get_book(url))
            print(i)


    def save_books_in_bd(self):
        urls = self.get_urls()
        threads = list()
        size = len(urls)
        thread_count = 20
        for index in range(thread_count):
            start = size // thread_count * index
            stop = min(size // thread_count * (index + 1), size)
            thr = threading.Thread(target=self.get_books, args=(urls[start:stop],))
            threads.append(thr)
            thr.start()
        for thr in threads:
            thr.join()