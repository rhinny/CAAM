from django.urls import path
from . import views

urlpatterns = [path('calendario/', views.calendario, name="calendario"),
               path('guardar_fechas/', views.guardar_fechas, name="guardar_fechas"),
               path('borrar_fechas/', views.borrar_fechas, name="borrar_fecha")
               ]