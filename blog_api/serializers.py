# todo/todo_api/serializers.py
from rest_framework import serializers
from .models import Blog, Author
from django.contrib.sites.models import Site
import base64
from django.core.files.base import ContentFile
import uuid

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "designation"]

class Base64FileField(serializers.FileField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:'):
            format, data = data.split(';base64,')
            ext = format.split('/')[-1] 
        return super().to_internal_value(ContentFile(base64.b64decode(data), name='{}.{}'.format(uuid.uuid4(), ext)))


class BlogSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    blog_image = Base64FileField()

    class Meta:
        model = Blog
        fields = ["id", "title", "description", "timestamp", "author", "blog_image", "updated"]

    def get_blog_image(self, obj):
        request = self.context.get('request')
        if request:
            protocol = 'https://' if request.is_secure() else 'http://'
            return protocol + Site.objects.get_current().domain + obj.blog_image.url
        return obj.blog_image.url


    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author = Author.objects.create(**author_data)
        blog = Blog.objects.create(author=author, **validated_data)
        return blog
    
    def update(self, instance, validated_data):
        # Update Author information if provided
        if 'author' in validated_data:
            author_data = validated_data.pop('author')
            author = instance.author  # Use existing author instance associated with instance
            author.name = author_data.get('name', author.name)
            author.designation = author_data.get('designation', author.designation)
            author.save()  # Save author changes

        # Update instance attributes
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()  # Save instance changes

        return instance