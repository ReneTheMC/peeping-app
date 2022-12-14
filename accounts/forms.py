from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder':('Username')})
        self.fields['email'].widget.attrs.update({'placeholder':('email')})
        self.fields['password1'].widget.attrs.update({'placeholder':('password')})
        self.fields['password2'].widget.attrs.update({'placeholder':('repeat password')})

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class EditAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

    def __init__(self, *args, **kwargs):
        super(EditAvatarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class EditInformationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']