from django.shortcuts import render, redirect
from datetime import date, timedelta
from .models import FechasDisponibles

# Create your views here.

def calendario(request):
    # Obtener mes actual
    hoy = date.today() #fecha actual
    primer_dia = hoy.replace(day=1) #primer día del mes actual
    ultimo_dia = (primer_dia.replace(month=hoy.month % 12 + 1, day=1) - timedelta(days=1)) #último día del mes actual
    
    # Generar lista de días del mes
    dias = [primer_dia + timedelta(days=i) for i in range((ultimo_dia - primer_dia).days + 1)]

    # Obtener eventos del mes
    eventos = FechasDisponibles.objects.filter(fecha__month=hoy.month)

    # Crear diccionario con días y eventos
    calendario = []
    for dia in dias:
        eventos_dia = [e for e in eventos if e.fecha == dia]
        calendario.append({"fecha": dia, "eventos": eventos_dia})

    return render(request, "calendario.html", {"calendario": calendario, "mes": hoy.strftime("%B")})
