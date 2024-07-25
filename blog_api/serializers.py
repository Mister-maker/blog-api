# todo/todo_api/serializers.py
from rest_framework import serializers
from .models import Blog, Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "designation"]

class BlogSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    class Meta:
        model = Blog
        fields = ["id", "title", "description", "timestamp", "updated", "author"]

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