from django.contrib.auth.models import AbstractUser
from django.db import models


class Abstract(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)

    class Meta:
        abstract = True


class User(AbstractUser):
    image = models.ImageField(upload_to='avatars', default=None)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='following', default=None)
    followers = models.ManyToManyField(User, related_name='followers', default=None)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    img = models.ImageField(upload_to='images')
    like = models.ManyToManyField(User, related_name='like')


class Comment(models.Model):
    text = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
