from django import forms
from django.contrib.auth.forms import UserCreationForm
from register.models import User


class RegisterForm(UserCreationForm):
    display_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['email', 'display_name', 'password1', 'password2']
