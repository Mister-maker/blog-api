from django.db import models

# Create your models here.

# todo/todo_api/models.py
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length = 180, blank=True, null=True)
    designation = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length = 180, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    blog_image = models.ImageField(upload_to = 'blog_images', blank = True, null = True)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated = models.DateTimeField(auto_now = True, blank = True)
    author = models.ForeignKey(Author, on_delete = models.CASCADE, related_name='author', blank = True, null = True)

    def __str__(self):
        return self.title
    

