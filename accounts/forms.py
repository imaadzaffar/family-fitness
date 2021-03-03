from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class CustomSignupForm(SignupForm):
    name = forms.CharField(
        help_text='This name will be shown on your family leaderboard by default',
        widget=forms.TextInput(attrs={'placeholder': 'Name'}),
        max_length=150
    )

    class Meta:
        model = User
        fields = ('email', 'name', 'password1', 'password2')

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        # Add your own processing here.
        user.name = self.cleaned_data['name']
        user.save()

        # You must return the original result.
        return user
