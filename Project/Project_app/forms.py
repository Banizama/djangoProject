from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User


class RegUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'date_of_birth', 'password1', 'password2')

    'USERNAME_FIELD'

