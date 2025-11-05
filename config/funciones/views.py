from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import date, timedelta, datetime
from .models import FechasDisponibles, Publi
from django.views.decorators.csrf import csrf_exempt
from app.models import Usuarios
from .forms import *
from django.contrib.auth.decorators import login_required
from app.forms import *
from app.models import *

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


#@csrf_exempt
def guardar_fechas(request):
    if request.method == "POST":
        fecha = request.POST.get('fecha')
        if fecha:
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            FechasDisponibles.objects.get_or_create(usuario=request.user, fecha=fecha_obj)
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

#@csrf_exempt
def borrar_fechas(request):
    if request.method == "POST":
        fecha = request.POST.get('fecha')
        if fecha:
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            FechasDisponibles.objects.filter(usuario=request.user, fecha=fecha_obj).delete()
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

@login_required
def publicar(request):
    usuario = request.user
    if not usuario.es_estudiante():
        return render(request, 'no_autorizado.html')
    
    if request.method=='POST':
        comuna_form = ComunaForm(request.POST, instance=usuario)
        seleccion_form = SeleccionForm(request.POST)
        publi_form = PubliForm(request.POST)
        if publi_form.is_valid() and seleccion_form.is_valid() and comuna_form.is_valid:
            Publi.objects.filter(usuario=request.user).delete() #borrar el post anterior
            publi = publi_form.save(commit=False)
            publi.usuario = usuario
            publi.save()
            comuna_form.save()
            usuario.areas.set(seleccion_form.cleaned_data['areas'])
            return redirect ('perfil_estudiante') # perfil estudiantes
    else:
        publi_form = PubliForm(initial={'titulo':usuario.username})
        comuna_form = ComunaForm(instance=usuario)
        seleccion_form = SeleccionForm(initial={'areas':usuario.areas.all()})
    return render(request, 'publicar.html', {"publi_form": publi_form,
        "comuna_form": comuna_form,
        "seleccion_form": seleccion_form})

@login_required
def editar_fechas(request):
    usuario = request.user
    if not usuario.es_estudiante():
        return render(request, "no_autorizado.html")
    return render(request, "perfil/editar_fechas.html")

def fechas_usuario(request):
    usuario = request.user
    fechas = FechasDisponibles.objects.filter(usuario=usuario)
    eventos = [{
            "title": "Disponible",
            "start": fecha.fecha.isoformat(),
            "allDay": True}
        for fecha in fechas
    ]
    return JsonResponse(eventos, safe=False)


@csrf_exempt
@login_required
def borrar_fecha(request): # repite la función de borrar fechas pero para editarlas luego, no me dejaba hacerlo de otra forma :(
    if request.method == "POST":
        fecha_str = request.POST.get("fecha")
        try:
            fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            FechasDisponibles.objects.filter(usuario=request.user, fecha=fecha_obj).delete()
            return JsonResponse({"status": "ok"})
        except ValueError:
            return JsonResponse({"status": "invalid date"}, status=400)
    return JsonResponse({"status": "invalid method"}, status=405)


@login_required
def perfil_estudiante(request):
    usuario = request.user
    if not usuario.es_estudiante():
        return render(request, "no_autorizado.html")
    publi = Publi.objects.filter(usuario=usuario).first()
    fechas = FechasDisponibles.objects.filter(usuario=usuario).order_by("fecha")

    return render(request, "perfil/perfil_estudiante.html", {
        "publi": publi,
        "fechas": fechas,
        "usuario": usuario,})

#función para que muestre los perfiles de los estudiantes a los adultos mayores
#filtro por áreas y comuna
def elegir(request):
    comuna_adultoM = request.user.comuna
    estudiantes = Usuarios.objects.filter(tipo="ESTUDIANTE")
    lista = []
    for estudiante in estudiantes:
        if estudiante.comuna == comuna_adultoM:
            voluntario = Publi.objects.get(usuario=estudiante)
            lista.append([voluntario.usuario, voluntario.descripcion])
    return render(request, "elegir.html", {"lista":lista})

#muestra calendario para agendar el día y la razón de la cita, opción de imprimir comprobante de cita
#envíar notificación al estudiante
def agendar_citas(request):
    #...
    return render(request, "agendar_citas.html")

#muestra las citas que tienen agendadas tanto los adultos mayores como los estudiantes
def ver_citas(request):
    #...
    return render(request, "perfil/ver_citas.html")

#cuando se cumplan cierta cantidad de citas el estudiante puede imprimir un certificado
def certificados(request):
    #...
    return render(request, "perfil/certificados.html")