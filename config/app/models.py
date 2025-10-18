from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

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

    def es_estudiante(self):
        return self.tipo == "ESTUDIANTE"
    
    def es_adulto_mayor(self):
        return self.tipo == "ADULTO_MAYOR"

'''
class Estudiante_log(models.Model):
    nombre_completo = models.CharField(max_length=50)
    correo_estudiante = models.CharField(max_length=50, primary_key=True)
    contraseña = models.CharField(max_length=50) #relacionarla con la base de datos,

    def __str__(self):
        return f"{self.correo_estudiante} ({self.rol})"
    
class AdultoM_log(models.Model):
    correo_adulto = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=50)
    rut = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return f"{self.correo_adulto} ({self.rut})"

Revisar error
class Cita(models.Model):
    id_cita=models.AutoField(primary_key=True)
    correo_adulto= models.CharField(max_length=50)
    estudiante = models.ForeignKey(Estudiante_log, on_delete=models.CASCADE)
    fecha_inicio= models.DateField() #API (en lugar de api usar SMTP django mail)
    fecha_termino= models.DateField() #API

    def __str__(self):
        return f"cita con: {self.estudiante.correo_estudiante} - ({self.estudiante.rol})"

'''
