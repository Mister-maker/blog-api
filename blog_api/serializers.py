# todo/todo_api/serializers.py
from rest_framework import serializers
from .models import Blog, Author
from django.contrib.sites.models import Site

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "designation"]

class BlogSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    blog_image = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ["id", "title", "description", "blog_image", "timestamp", "updated", "author"]

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