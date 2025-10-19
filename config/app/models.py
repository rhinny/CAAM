from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Area(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Usuarios(AbstractUser):
    rut = models.CharField(max_length=12, primary_key=True)
    TIPOS = [("ESTUDIANTE","Estudiante"),
    ("ADULTO_MAYOR","Adulto Mayor")]   
    tipo = models.CharField(max_length=20, choices=TIPOS)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True, blank=True)
    areas = models.ManyToManyField(Area, blank=True)

    def es_estudiante(self):
        return self.tipo == "ESTUDIANTE"
    
    def es_adulto_mayor(self):
        return self.tipo == "ADULTO_MAYOR"


