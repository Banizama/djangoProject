from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User, Post, Comment


class LoginForm(AuthenticationForm):


    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        widgets = {'username': forms.TextInput(attrs={'id': 'username'}),
                   'password1': forms.PasswordInput(attrs={'id': 'password1'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'input'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['class'] = 'input'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'


class RegUserForm(UserCreationForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input', 'type':'text',  'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input', 'type':'text',  'placeholder': 'Confirm password'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets={
            'username': forms.TextInput(attrs={'class': 'input', 'type': 'text',  'placeholder': 'Username'}),
            'email':forms.EmailInput(attrs={'class': 'input', 'type': 'text',  'placeholder': 'Email'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords aren\'t equal')
        return cd['password1']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already used')
        return email


# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         fields = ('text',)
#         widgets = {'text': forms.Textarea(attrs={'id': 'message'})}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('img', 'description')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {'text': forms.TextInput(attrs={'id': 'comment'})}
