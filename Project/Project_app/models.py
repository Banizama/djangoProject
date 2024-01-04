from django.db import models


class Abstract(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    image = models.ImageField(upload_to='static/images', default='static/images/default_user_img.jpg')
    date_of_birth = models.DateTimeField()

    class Meta:
        abstract = True

    
class User(Abstract):
    password = models.CharField(max_length=100)


class Friend(Abstract):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    img = models.ImageField(upload_to='static/images')



