# Generated by Django 5.0.7 on 2024-07-22 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_api', '0003_alter_blog_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='blog_image',
            field=models.ImageField(blank=True, null=True, upload_to='blog_images'),
        ),
    ]
