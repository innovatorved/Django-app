from django.forms import ModelForm , Form
from django import forms
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class LoginForm(Form):
    username = forms.CharField(label='username', max_length=100)
    pwd = forms.CharField(label='Password' , max_length=20, widget=forms.PasswordInput)