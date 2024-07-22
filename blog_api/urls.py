from django.urls import path
from .views import (
    BlogListApiView,
    BlogDetailApiView
)

urlpatterns = [
    path('api/', BlogListApiView.as_view(), name='list_api'),
    path('api/<int:blog_id>/', BlogDetailApiView.as_view()),
]