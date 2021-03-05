from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, EmailInput
from django import forms



class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'password'}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm your password'}),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={
                "class": "form-control",
                "type": "text",
                "name": "username",
                "placeholder": "Username",
            }),
            'first_name': TextInput(attrs={
                "class": "form-control",
                "type": "text",
                "name": "first_name",
                "placeholder": "First Name",
            }),
            'last_name': TextInput(attrs={
                "class": "form-control",
                "type": "text",
                "name": "last_name",
                "placeholder": "Last Name",
            }),
            'email': EmailInput(attrs={
                "class": 'form-control',
                "type": "email",
                "name": "email",
                "placeholder": "Email",

            }),
        }


