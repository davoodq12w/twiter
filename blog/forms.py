from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    image = forms.ImageField(allow_empty_file=True, label='add image', widget=forms.FileInput(
        attrs={'placeholder': 'add image', 'class': 'add-image'}))

    class Meta:
        model = Post
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'add-post-title'}),
            'description': forms.Textarea(attrs={'class': 'add-post-description'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'username-input', 'placeholder': 'username'}), label='username')
    password = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'password-input', 'placeholder': 'password'}), label='password')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['auther', 'text']
        widgets = {
            'auther': forms.TextInput(attrs={'class': 'add-comment-auther'}),
            'text': forms.Textarea(attrs={'class': 'add-comment-text'}),
        }


class SearchForm(forms.Form):
    query = forms.CharField()


class AddAccountForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'username', 'class': 'username-input'}))
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(
        attrs={'placeholder': 'password', 'class': 'password-input'}))
    confirm_password = forms.CharField(min_length=8, widget=forms.PasswordInput(
        attrs={'placeholder': 'confirm password', 'class': 'password-input'}))


class EditProfileForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'new username', 'class': 'new-username'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'new password', 'class': 'new-password'}))
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'confirm new password', 'class': 'new-password'}))
