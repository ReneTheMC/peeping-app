from django import forms
from django.forms import ModelForm

from posts.models import Post


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']