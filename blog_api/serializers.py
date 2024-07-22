# todo/todo_api/serializers.py
from rest_framework import serializers
from .models import Blog
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["id", "title", "description", "blog_image", "timestamp", "updated", "author"]