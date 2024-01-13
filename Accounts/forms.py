from django import forms
from .models import UserProfileModel, UserPost, PostComment


class UserProfileEdit(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = UserProfileModel
        fields = ('bio', 'age')

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'style': 'resize:none;'})
        }


class UserPostCreateForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control', 'style': 'resize:none;', 'placeholder': 'Type your post please ...'
            })
        }
        labels = {
            'body': ''
        }


class PostCommentCreateForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control', 'style': 'resize:none;', 'placeholder': 'Write your comment here ...', 'rows': 2
            })
        }
        labels = {
            'body': ''
        }


class CommentReplayForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ('replay', 'body')

        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control', 'style': 'resize:none;', 'placeholder': 'Write your comment here ...',
                'rows': 2,
            }),
        }

        labels = {
            'body': ''
        }
