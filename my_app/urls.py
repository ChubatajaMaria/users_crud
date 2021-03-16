from django.urls import re_path, path
from .api import UserManageView, UserRUDApi, LoginAPIView

urlpatterns = [
    re_path('^users/?$', UserManageView.as_view(), name='users'),
    re_path(r'^users/(?P<pk>\d+)/?$', UserRUDApi.as_view(), name='user'),
    re_path('^api-token-auth/?$', LoginAPIView.as_view(), name='login'),
]
