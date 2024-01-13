from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password_confirm = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    def clean_username(self):
        form_username = self.cleaned_data['username']
        user_username = User.objects.filter(username=form_username)
        if user_username.exists():
            raise ValidationError('This username is already Exists ... !')
        else:
            return form_username

    def clean_email(self):
        form_email = self.cleaned_data['email']
        user_email = User.objects.filter(email=form_email)
        if user_email.exists():
            raise ValidationError('This email is already Exists ... !')
        else:
            return form_email

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password')
        p2 = cd.get('password_confirm')
        if p1 != p2:
            raise ValidationError('Passwords are not the Same !!')


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Username or Email', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class UserSearchBox(forms.Form):
    search_user = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search Username ...'}))


class PostSearchBox(forms.Form):
    post_search = forms.CharField(label= '', widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'Search a word or a sentence of the post ...', 'rows': 1, 'style': 'resize:none;'
    }))
