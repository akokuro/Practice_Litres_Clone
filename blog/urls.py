from django.urls import re_path, include  
from .views import BlogViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'write', BlogViewSet, basename='Blog')
urlpatterns = router.urls