from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True)

    field_order = ['username', 'email', 'password1', 'password2']

    class Meta:
        model = User
        fields = {'username', 'email', 'password1', 'password2'}