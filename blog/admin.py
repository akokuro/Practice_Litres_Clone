from django.contrib import admin

# Register your models here.

from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['headline']