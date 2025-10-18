from django.db import models
from app.models import Usuarios

# Create your models here.

class FechasDisponibles(models.Model):
    #nombre_persona = models.CharField(max_length=100)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"{self.nombre_persona} - {self.fecha} {self.hora}"
