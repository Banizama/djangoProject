from django.db import models

# Create your models here.

class Post(models.Model):
    description = models.CharField(max_length=200)
    img = models.ImageField(upload_to='static/images')


class Abstract(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    image = models.ImageField(upload_to='static/images')
    date_of_birth = models.DateTimeField()
    class Meta():
        abstract = True

    
class User(Abstract):
    password = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Friend(Abstract):
    user = models.ForeignKey(User, on_delete=models.CASCADE)



