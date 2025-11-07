from django.urls import path
from . import views

urlpatterns = [path('calendario/', views.calendario, name="calendario"),
               path('guardar_fechas/', views.guardar_fechas, name="guardar_fechas"),
               path('borrar_fechas/', views.borrar_fechas, name="borrar_fecha"),
               path('publicar/', views.publicar, name="publicar"),
               path('editar_fechas/', views.editar_fechas, name='editar_fechas'),
               path('perfil/perfil_estudiante/', views.perfil_estudiante, name='perfil_estudiante'),
               path('fechas/', views.fechas_usuario, name='fechas_usuario'),
               path('adulto_mayor/', views.elegir, name='elegir'),
               path('agendar_citas/<str:estudiante_id>', views.agendar_citas, name='agendar_citas'),
               path('citas/', views.ver_citas, name='ver_citas'),
               path('certificado/', views.certificados, name='certificados'),
               ]