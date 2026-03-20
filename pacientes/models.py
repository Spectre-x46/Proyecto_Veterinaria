from django.db import models

class Propietario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50, null=True, blank=True)
    telefono_contacto = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Paciente representa a una mascota que es atendida en la clínica veterinaria. Cada paciente tiene un nombre, especie, raza (opcional), fecha de nacimiento, fecha de registro automática y está asociado a un propietario.
class Paciente(models.Model):
    ESPECIES = [
        ('PERRO', 'Perro'),
        ('GATO', 'Gato'),
        ('AVE', 'Ave'),
        ('OTRO', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=20, choices=ESPECIES)
    raza = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField()
    fecha_registro = models.DateField(auto_now_add=True)
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='pacientes')