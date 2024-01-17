from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Post, Comment


class RegUserForm(UserCreationForm):
    username = forms.CharField(help_text='')
    email = forms.CharField(help_text='', widget=forms.EmailInput())
    password1 = forms.CharField(help_text='', widget=forms.PasswordInput())
    password2 = forms.CharField(help_text='', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('img', 'description')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
