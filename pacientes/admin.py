from django.contrib import admin
from .models import Propietario, Paciente

@admin.register(Propietario)
class PropietarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono_contacto')
    search_fields = ('nombre', 'telefono_contacto')

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'raza', 'fecha_nacimiento', 'fecha_registro', 'propietario')
    search_fields = ('nombre', 'raza', 'propietario__nombre')
    list_filter = ('especie', 'fecha_registro')
    