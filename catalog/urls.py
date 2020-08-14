from django.urls import re_path, include  
from .views import CatalogViewSet, FillDbAPIView
from rest_framework.routers import DefaultRouter

methods_dict = {
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
}

router = DefaultRouter()
router.register(r'catalog', CatalogViewSet, basename='Catalog')

urlpatterns = [
    re_path(r'^fill/?$', FillDbAPIView.as_view(), name='Fill'),
]

urlpatterns += router.urls