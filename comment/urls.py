from django.urls import re_path, include  
from .views import WriteCommentAPIView, GetLastSimilarBookCommentAPIView


urlpatterns = [
    re_path(r'^comment/?$', WriteCommentAPIView.as_view(), name='write_comment'),
    re_path(r'^reviews/?$', GetLastSimilarBookCommentAPIView.as_view(), name='view_three_last_comment'),
]