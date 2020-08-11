from django.urls import re_path, include  
from .views import BlogViewSet
from rest_framework.routers import DefaultRouter

methods_dict = {
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
}

router = DefaultRouter()
router.register(r'write', BlogViewSet, basename='Blog')
urlpatterns = router.urls

# urlpatterns = [
#     re_path(r'^write/?$', BlogViewSet.as_view(), name='user_blog'),
# ]