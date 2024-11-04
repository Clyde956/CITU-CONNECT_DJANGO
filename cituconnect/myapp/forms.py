from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('firstName', 'lastName', 'username', 'email', 'password1', 'password2', 'role', 'school')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'priorityLevel', 'isAnonymous', 'categoryId']
