# Generated by Django 5.0.7 on 2024-07-25 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_api', '0006_remove_author_blog_blog_auther'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='auther',
            new_name='author',
        ),
    ]