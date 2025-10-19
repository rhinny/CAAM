from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import date, timedelta, datetime
from .models import FechasDisponibles
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def calendario(request):
    # Obtener mes actual
    hoy = date.today() #fecha actual YYYY-MM-DD
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

@csrf_exempt
def guardar_fechas(request):
    if request.method == "POST":
        fecha = request.POST.get('fecha')
        if fecha:
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            FechasDisponibles.objects.get_or_create(estudiante=request.user, fecha=fecha_obj)
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

@csrf_exempt
def borrar_fechas(request):
    if request.method == "POST":
        fecha = request.POST.get('fecha')
        if fecha:
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            FechasDisponibles.objects.filter(estudiante=request.user, fecha=fecha_obj).delete()
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})