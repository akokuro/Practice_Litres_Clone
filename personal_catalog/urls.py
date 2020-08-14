from django.urls import re_path, include  
from .views import AddInPersonalCatalogAPIView, DeleteFromPersonalCatalogAPIView, PersonalCatalogAPIView


urlpatterns = [
    re_path(r'^add/?$', AddInPersonalCatalogAPIView.as_view(), name='add_in_personal_catalog'),
    re_path(r'^delete/?$', DeleteFromPersonalCatalogAPIView.as_view(), name='delete_from_personal_catalog'),
    re_path(r'^stat/?$', PersonalCatalogAPIView.as_view(), name='personal_catalog'),
]