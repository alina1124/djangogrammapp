from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Post, PostImage, Comment, Reply


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['main_image', 'caption']
        widgets = {
            'main_image': forms.FileInput(attrs={'class': 'form-control'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class PostImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'multiple': True}))

    class Meta:
        model = PostImage
        fields = ['image']
        labels = {
            'image': 'images'
        }

    def __init__(self, *args, **kwargs):
        super(PostImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Add a comment', 'style': 'resize:none;'}),
        }
        labels = {
            'body': ""
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        widgets = {
            'body': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Add a comment', 'style': 'resize:none;'}),
        }
        labels = {
            'body': ""
        }


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Username'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Your email'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Repeat your password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        error_messages = {'username': {'style': 'color: red;'}}


class UserLoginFrom(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control  form-control-lg', 'placeholder': 'username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control  form-control-lg', 'placeholder': 'password'}))
