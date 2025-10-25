from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
'''
class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['tipo','rut','username','email', 'password']
'''

class PubliForm(forms.ModelForm):
    class Meta:
        model = Publi
        fields = ['titulo', 'descripcion']
        labels = {
            'titulo': 'Título de la publicación',
            'descripcion': 'Contenido'
        }
        widgets= {
            'titulo': forms.TextInput(attrs={'class':'form-control','placeholder':'Escribe un titulo'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control','rows':5})
        }