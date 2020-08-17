from django.contrib import admin

# Register your models here.

from .models import ReadedBook, WantedBook

@admin.register(ReadedBook)
class ReadedBookAdmin(admin.ModelAdmin):
    search_fields = ['user_id__username', 'book_id__title']

@admin.register(WantedBook)
class WantedBookAdmin(admin.ModelAdmin):
    search_fields = ['user_id__username', 'book_id__title']