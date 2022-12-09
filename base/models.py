from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
from django.urls import reverse


def post_directory_path(instance, filename):
    return f'{instance.user.id}/posts/main_image/{filename}'


def content_directory_path(instance, filename):
    return f'{instance.post.user.id}/posts/contents/{filename}'


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    main_image = models.ImageField(upload_to=post_directory_path)
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('post-view', kwargs={'post_id': self.id})

    class Meta:
        ordering = ['-created_at']


class Tag(models.Model):
    caption = models.CharField(max_length=20)
    posts = models.ManyToManyField(Post, related_name='tags')

    def __str__(self):
        return self.caption

    def get_absolute_url(self):
        return reverse('tags', kwargs={'tag_name': self.caption})

    def get_posts(self):
        return "\n".join([p.caption[:30] for p in self.posts.all()])

    class Meta:
        ordering = ['-id']


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_image')
    image = models.ImageField(upload_to=content_directory_path)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)

    def __str__(self):
        return '%d - %s' % (self.id, self.user.username)


class Reply(models.Model):
    reply_to = models.ForeignKey(Comment, related_name='reply', blank=True, on_delete=models.CASCADE)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_user')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='reply_like', blank=True)
