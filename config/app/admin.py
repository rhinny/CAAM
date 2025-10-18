from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Usuarios)
admin.site.register(models.Comuna)
admin.site.register(models.Area)