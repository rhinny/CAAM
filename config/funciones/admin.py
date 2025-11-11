from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.FechasDisponibles)
class FechasDisponiblesAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'hora', 'disponible')
    list_filter = ('disponible', 'fecha')
    search_fields = ('usuario_username', 'usuario_rut')
    ordering = ('-fecha', 'hora')
admin.site.register(models.Publi)
admin.site.register(models.Cita)