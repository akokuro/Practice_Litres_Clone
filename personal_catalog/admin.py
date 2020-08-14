from django.contrib import admin

# Register your models here.

from .models import ReadedBook, WantedBook

admin.site.register(ReadedBook)
admin.site.register(WantedBook)