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

class ComunaForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['comuna']

class SeleccionForm(forms.Form): 
    areas = forms.ModelMultipleChoiceField(
        queryset=Area.objects.all(),
        widget= forms.CheckboxSelectMultiple,
        required=True,
        label = "Selecciona al menos tres area de apoyo:")
    
    def clean_areas(self):
        cantidad = self.cleaned_data.get('areas')
        if not cantidad or len(cantidad) < 3:
            raise forms.ValidationError("Seleccione al menos tres areas!")
        return cantidad

'''
formulario para que pida email o username
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Usuarios
        fields = ['email', 'password']
'''