from django.db import models

# Create your models here.


class Abstract(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    image = models.ImageField(upload_to='static/images')
    date_of_birth = models.DateTimeField()
    class Meta():
        abstract = True

    
class User(Abstract):
    password = models.CharField(max_length=100)


class Friend(Abstract):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
