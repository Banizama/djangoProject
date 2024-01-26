from django.contrib.auth import get_user_model
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
    username = forms.CharField(help_text='')
    email = forms.CharField(help_text='')
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {'username': forms.TextInput(attrs={'id': 'username'}),
                   'email': forms.EmailInput(attrs={'id': 'email'}),
                   'password1': forms.PasswordInput(attrs={'id': 'password1'}),
                   'password2': forms.PasswordInput(attrs={'id': 'password2'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'input'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['class'] = 'input'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['class'] = 'input'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'input'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat password'

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
