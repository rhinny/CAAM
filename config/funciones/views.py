from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from datetime import date, timedelta, datetime
from .models import FechasDisponibles, Publi
from django.views.decorators.csrf import csrf_exempt
from app.models import Usuarios, Area
from .forms import *
from django.contrib.auth.decorators import login_required
from app.forms import *
from app.models import *
from .pdfcreate import crear_pdf #pdfcreate
from django.utils import timezone
from django.shortcuts import render, redirect
from django.utils import timezone
from funciones.models import Cita

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
        campus_form = CampusForm(request.POST, instance=usuario)
        seleccion_form = SeleccionForm(request.POST)
        publi_form = PubliForm(request.POST)
        if publi_form.is_valid() and seleccion_form.is_valid() and comuna_form.is_valid() and campus_form.is_valid():
            Publi.objects.filter(usuario=request.user).delete() #borrar el post anterior
            publi = publi_form.save(commit=False)
            publi.usuario = usuario
            publi.save()
            comuna_form.save()
            campus_form.save()
            usuario.areas.set(seleccion_form.cleaned_data['areas'])
            return redirect ('perfil_estudiante') # perfil estudiantes
    else:
        publi_form = PubliForm(initial={'titulo':usuario.username})
        comuna_form = ComunaForm(instance=usuario)
        campus_form = CampusForm(instance=usuario)
        seleccion_form = SeleccionForm(initial={'areas':usuario.areas.all()})
    return render(request, 'publicar.html', {"publi_form": publi_form,
        "comuna_form": comuna_form,
        "seleccion_form": seleccion_form,
        "campus_form": campus_form,})

@login_required
def editar_fechas(request):
    usuario = request.user
    if not usuario.es_estudiante():
        return render(request, "no_autorizado.html")
    return render(request, "perfil/editar_fechas.html")

def fechas_usuario(request):
    usuario = request.user
    fechas = FechasDisponibles.objects.filter(usuario=usuario)
    eventos = []
    for fecha in fechas:
        if fecha.disponible:
            eventos.append({"title": "Disponible", "start": fecha.fecha.isoformat(), "allDay": True})
        else:
            eventos.append({"title": "Agendado", "start": fecha.fecha.isoformat(), "allDay": True, "backgroundColor": "red"})

    return JsonResponse(eventos, safe=False)


@login_required

def perfil_estudiante(request):
    usuario = request.user
    if not usuario.es_estudiante():
        return render(request, "no_autorizado.html")
    publi = Publi.objects.filter(usuario=usuario).first()
    fechas = FechasDisponibles.objects.filter(usuario=usuario).order_by("fecha")
    citas = Cita.objects.filter(estudiante=usuario).select_related("adulto_mayor", "fecha")

    #Contar cuantas citas ya fueron completadas
    total_citas_cumplidas = sum(1 for cita in citas if cita.fecha.fecha < timezone.now().date())
    tiene_certificado = total_citas_cumplidas >= 8
    tipo = "adulto" if usuario.es_adulto_mayor() else "estudiante"
    
    return render(request, "perfil/perfil_estudiante.html", {
        "publi": publi,
        "fechas": fechas,
        "usuario": usuario,
        "citas": citas,
        "tipo":tipo,
        "tiene_certificado": tiene_certificado,
        })

#función para que muestre los perfiles de los estudiantes a los adultos mayores
#filtro por áreas y comuna
@login_required
def elegir(request):
    comuna_adultoM = request.user.comuna
    areas_adultoM = [area.nombre for area in request.user.areas.all()]
    estudiantes = Usuarios.objects.filter(tipo="ESTUDIANTE")
    lista = []
    for estudiante in estudiantes:
        voluntario = Publi.objects.get(usuario=estudiante)
        if estudiante.comuna == comuna_adultoM:
            areas_estudiante = [area.nombre for area in estudiante.areas.all()]
            for area in areas_adultoM:
                if area in areas_estudiante and [estudiante, voluntario, areas_estudiante] not in lista:
                    lista.append([estudiante, voluntario, areas_estudiante])
    tipo = "adulto" if request.user.es_adulto_mayor() else "estudiante"
    return render(request, "elegir.html", {"lista":lista,"tipo":tipo})

@login_required
def agendar_citas(request, estudiante_id):
    adultoM = request.user
    if not adultoM.es_adulto_mayor():
        return render(request, "no_autorizado.html")

    estudiante = get_object_or_404(Usuarios, rut=estudiante_id)
    publi = Publi.objects.filter(usuario=estudiante).first()
    email = estudiante.email
    fechas = FechasDisponibles.objects.filter(usuario=estudiante).order_by("fecha")
    if request.method == "POST":
        fecha_id = request.POST.get("fecha_id")
        fecha = get_object_or_404(FechasDisponibles, id=fecha_id, usuario=estudiante)
        if fecha.disponible:
            fecha.disponible = False
            fecha.save()
            '''
            Cita.objects.update_or_create(
                estudiante=estudiante,
                adulto_mayor=adultoM,
                defaults={"fecha": fecha, "email":email}
            )
            '''
            Cita.objects.update_or_create(
                estudiante = estudiante, 
                adulto_mayor = adultoM,
                fecha  = fecha
            )
            return redirect("mis_citas")
    tipo = "adulto" if request.user.es_adulto_mayor() else "estudiante"
    return render(request, "agendar_citas.html", {
        "estudiante": estudiante,
        "publi": publi,
        "fechas": fechas,
        "tipo":tipo,
    })

@login_required
def mis_citas(request):
    usuario = request.user
    if usuario.es_adulto_mayor():
        citas = Cita.objects.filter(adulto_mayor=usuario).select_related("estudiante", "fecha")
        return render(request, "perfil/ver_citas.html", {"citas": citas})
    elif usuario.es_estudiante():
        citas = Cita.objects.filter(estudiante=usuario).select_related("adulto_mayor", "fecha")
        publi = Publi.objects.filter(usuario=usuario).first()
        fechas = FechasDisponibles.objects.filter(usuario=usuario).order_by("fecha")
        return render(request, "perfil/perfil_estudiante.html", {
            "usuario": usuario,
            "publi": publi,
            "fechas": fechas,
            "citas": citas
        })
    tipo = "adulto" if request.user.es_adulto_mayor() else "estudiante"
    return render(request, "no_autorizado.html",{"tipo":tipo,})





'''
#muestra calendario para agendar el día y la razón de la cita, opción de imprimir comprobante de cita
#envíar notificación al estudiante
def agendar_citas(request):
    adultoM = request.user
    if adultoM.es_estudiante():
        return render(request, "no_autorizado.html")
    return render(request, "agendar_citas.html")


def cita_calendario(request):
    estudiante = get_object_or_404(Usuarios, rut.estudiante_id, tipo="ESTUDIANTE")
    publi = Publi.objects.filter(usuario=estudiante)
    fechas = FechasDisponibles.objects.filter(usuario=estudiante).order_by("fecha")
    if request.method == "POST":
        fecha_id = request.POST.get("fecha_id")
        fecha = get_object_or_404(FechasDisponibles, id=fecha_id, usuario=estudiante)
        Cita.objects.update_or_create(
            voluntario = estudiante
            adultoM = request.user)
            defaults = {"fecha":fecha}
        return redirect("cita_confirmada") #extiende el html de ver perfil
    return render(request, "agendar_citas.html",{"estudiante":estudiante,"publi":publi,"fechas":fechas})
'''

#muestra las citas que tienen agendadas tanto los adultos mayores como los estudiantes
def ver_citas(request):
    #...
    return render(request, "perfil/ver_citas.html")

#cuando se cumplan cierta cantidad de citas el estudiante puede imprimir un certificado
def certificados(request):
    usuario = request.user

    #Verificar que el usuario esté autenticado
    if not usuario.is_authenticated:
        return redirect('login')
    #Obtener todas las citas del usuario
    citas_usuario = Cita.objects.filter(estudiante=usuario)
    #Contar solo las que ya se cumplieron
    total_citas_cumplidas = sum(
        1 for cita in citas_usuario if cita.esta_completada()
        )
    #Verificar si ya puede obtener el certificado
    tiene_certificado = total_citas_cumplidas >= 8

    context = {
        "tiene_certificado": tiene_certificado,
        "total_citas": total_citas_cumplidas
    }
    
    return render(request, "perfil/certificados.html", context)