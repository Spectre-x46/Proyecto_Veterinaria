from django.shortcuts import render
from .models import Paciente
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import PacienteForm
# R: READ (lista de pacientes)
# SELECT * FROM tabla;
class PacienteListView(ListView):
    model = Paciente
    template_name = 'pacientes/paciente_list.html'
    context_object_name = 'pacientes'

class PacienteCreateView(CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/paciente_form.html'
    success_url = reverse_lazy('paciente_list')
    success_message = "Paciente creado exitosamente."

class PacienteUpdateView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/paciente_form.html'
    success_url = reverse_lazy('paciente_list')
    success_message = "Paciente actualizado exitosamente."

class PacienteDeleteView(DeleteView):
    model = Paciente
    success_url = reverse_lazy('paciente_list')

    def form_valid(self, form):
        messages.success(self.request, "Paciente eliminado exitosamente.")
        return super().form_valid(form)