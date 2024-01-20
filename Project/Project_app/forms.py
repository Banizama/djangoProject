from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Post, Comment



class RegUserForm(UserCreationForm):
    username = forms.CharField(help_text='')
    email = forms.CharField(help_text='', widget=forms.EmailInput())
    password1 = forms.CharField(help_text='', widget=forms.PasswordInput())
    password2 = forms.CharField(help_text='', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t equal')
        return cd['password1']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already used')
        return email


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('img', 'description')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
