from django.db import models
from app.models import Usuarios
from django.utils import timezone

# Create your models here.

class FechasDisponibles(models.Model):
    #nombre_persona = models.CharField(max_length=100)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField()
    hora = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario} - {self.fecha} {self.hora}"
    

class Publi(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(default=timezone.now)
    titulo = models.TextField(max_length=50)
    descripcion = models.TextField(max_length=200)
    
    def __str__(self):
        return f"{self.titulo} {(self.usuario)}"
    
    def tag_area(self):
        return self.usuario.areas.all()
    
    def tag_comuna(self):
        return self.usuario.comuna.nombre
    