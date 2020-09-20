from django import forms
from .models import Post, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user_comment']


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'text']
