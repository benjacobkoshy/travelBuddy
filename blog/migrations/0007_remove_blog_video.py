# Generated by Django 5.0.2 on 2024-04-13 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_comment_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='video',
        ),
    ]
