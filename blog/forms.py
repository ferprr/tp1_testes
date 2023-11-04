from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    pass

class PostForm(forms.ModelForm):

  class Meta:
    model = Post
    fields = ('title', 'subtitle', 'category','text')

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']