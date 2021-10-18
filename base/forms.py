from django.forms import ModelForm , Form
from django import forms
from .models import Room

# user creation form
from django.contrib.auth.forms import UserCreationForm

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class LoginForm(Form):
    username = forms.CharField(label='username', max_length=100)
    pwd = forms.CharField(label='Password' , max_length=20, widget=forms.PasswordInput)

class CreateUser:
    """ Create user form 
    Fields :
       - username
       - password
       - Email
       - first_name
       - last_name

       Initialize with CreateUser.form
    """
    form = UserCreationForm
