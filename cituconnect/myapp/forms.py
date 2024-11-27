from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post, School

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('firstName', 'lastName', 'username', 'email', 'password1', 'password2', 'role', 'school')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'priorityLevel', 'isAnonymous', 'categoryId', 'image']

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    school = forms.ModelChoiceField(queryset=School.objects.all(), required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'school', 'profile_picture', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")