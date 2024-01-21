from django.contrib.auth.models import AbstractUser
from django.db import models


class Abstract(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    image = models.ImageField(upload_to='static/images', default='media/images/default_user_img.jpg')

    class Meta:
        abstract = True


class User(AbstractUser):
    pass


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='following', default=None)
    followers = models.ManyToManyField(User, related_name='followers', default=None)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    description = models.CharField(max_length=200)
    img = models.ImageField(upload_to='images')


class Comment(models.Model):
    text = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='Like', default=None, null=True)