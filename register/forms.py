
from dataclasses import fields
from django import forms
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["first_name","last_name","email","username","password1",'password2']



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["first_name","last_name","email","username"]

