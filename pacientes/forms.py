from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'especie', 'raza', 'fecha_nacimiento', 'propietario']
        # Widgets sirven para agregar clases css a los campos del formulario, lo que facilita su estilización en el frontend.
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}), # <input type="text" class="form-control">
            'especie': forms.Select(attrs={'class': 'form-control'}), # <select class="form-control">...</select>
            'raza': forms.TextInput(attrs={'class': 'form-control'}), # <input type="text" class="form-control">
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), # <input type="date" class="form-control">
            'propietario': forms.Select(attrs={'class': 'form-control'}), # <select class="form-control">...</select>
        }