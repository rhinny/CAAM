from django.db import models
from app.models import Usuarios
from django.utils import timezone

# Create your models here.

class FechasDisponibles(models.Model):
    #nombre_persona = models.CharField(max_length=100)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField()
    disponible = models.BooleanField(default=True)
    hora = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario} - {self.fecha} {self.hora}"
    

class Publi(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    titulo = models.TextField(max_length=50)
    descripcion = models.TextField(max_length=200)
    
    def __str__(self):
        return f"{self.titulo} {(self.usuario)}"
    
    def tag_area(self):
        return self.usuario.areas.all()
    
    def tag_comuna(self):
        return self.usuario.comuna.nombre

class Cita(models.Model):
    estudiante = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name="matches_recibidos")
    adulto_mayor = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name="matches_realizados")
    fecha = models.ForeignKey(FechasDisponibles, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    def esta_completada(self):
        return self.fecha.fecha < timezone.now().date()




'''
por implementar en el push
class Cita():
    estudiante = models.ForeignKey(
    Usuarios,
    on_delete=models.CASCADE,
    limit_choices_to={"es_estudiante": True},
    )
    adultoM = models.ForeignKey(
    Usuarios,
    on_delete=models.CASCADE,
    limit_choices_to={"es_adulto_mayor": True},
    )
    fechas = models.DateField()
    #def completo
    #def incompleto
'''