from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuarios
        fields = ['tipo','rut','email','username', 'first_name', 'last_name', 'password1','password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

class ComunaForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['comuna']

class CampusForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['campus']

class SeleccionForm(forms.Form): 
    areas = forms.ModelMultipleChoiceField(
        queryset=Area.objects.all(),
        widget= forms.CheckboxSelectMultiple,
        required=True,
        label = "Selecciona al menos tres areas:")
    
    
    def clean_areas(self):
        cantidad = self.cleaned_data.get('areas')
        if not cantidad or len(cantidad) < 3:
            raise forms.ValidationError("Seleccione al menos tres areas!")
        return cantidad
