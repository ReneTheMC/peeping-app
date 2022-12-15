from django import forms
from django.forms import ModelForm

from posts.models import Post


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class EditPostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['image', 'caption']

    def __init__(self, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
