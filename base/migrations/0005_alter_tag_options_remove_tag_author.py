# Generated by Django 4.1.3 on 2022-11-12 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_remove_post_likes_delete_likepost_post_likes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-id']},
        ),
        migrations.RemoveField(
            model_name='tag',
            name='author',
        ),
    ]
