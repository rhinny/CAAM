from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
'''
class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['tipo','rut','username','email', 'password']

class AdultoMForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['tipo','rut', 'username', 'email','password']
'''
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuarios
        fields = ['tipo','rut','email','username','password1','password2']

'''
formulario para que pida email o username
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Usuarios
        fields = ['email', 'password']
'''