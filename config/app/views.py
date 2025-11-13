from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import Usuarios
from funciones.urls import *

def home(request):
    contexto = {'texto':"Home"}
    persona = request.user
    if persona.is_authenticated:
        usuario = True 
    else:
        usuario = False
    contexto["usuario"] = usuario
    contexto["persona"] = persona
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
            user = form.get_user()
            if user.tipo == 'ESTUDIANTE':
                return redirect("perfil_estudiante") # Redirigir al home de estudiante
            else:
                return redirect("elegir") # Redirigir al home de adultom
    else:
        form = AuthenticationForm()
    return render(request, "usuarios/login.html", {'form':form})

def logout_view(request):
    logout(request)
    return redirect('home')

def comuna(request):
    if request.method == "POST":
        form = ComunaCampusForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if request.user.tipo == "ESTUDIANTE":
                return redirect("publicar") 
            else:
                return redirect("elegir") 
    else:
        form = ComunaCampusForm(instance=request.user)
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


