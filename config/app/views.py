from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import Usuarios
from funciones.urls import *

def home(request):
    contexto = {'texto':"Home"}
    return render(request, "home.html",contexto)

def registro(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("seleccion")
    else:
        form = CustomUserCreationForm()
    return render(request, "usuarios/registro.html", {'form':form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if Usuarios.tipo == "ESTUDIANTE":
                return redirect("perfil_estudiante") # Redirigir al home de estudiante
            else:
                return redirect("home") # Redirigir al home de adultom
    else:
        form = AuthenticationForm()
    return render(request, "usuarios/login.html", {'form':form})

def comuna(request):
    if request.method == "POST":
        form = ComunaForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if request.user.tipo == "ESTUDIANTE":
                return redirect("publicar") #debería redirigir a selección de fechas disponibles
            else:
                return redirect("home") #debería redirigir a /adultomayor (según diseño)
    else:
        form = ComunaForm(instance=request.user)
        form.fields['comuna'].queryset = Comuna.objects.all().order_by('nombre')
    if request.user.tipo == "ESTUDIANTE":
        return render(request, "usuarios/estudiantes/comuna_disponibilidad.html", {'form':form})
    else:
        return render(request, "usuarios/adultom/comuna.html", {'form':form})

def seleccion(request):
    if request.method == "POST":
        form = SeleccionForm(request.POST)
        if form.is_valid():
            request.user.areas.set(form.cleaned_data['areas'])
            return redirect ("comuna") # Redirigir a comuna
    else:
        form = SeleccionForm(request.POST)
    return render(request, "usuarios/seleccion.html", {'form':form})


