# Proyecto Veterinaria - Sistema de Gestión

Este proyecto es una aplicación de gestión para una clínica veterinaria desarrollada con **Django 6.0.3** y **PostgreSQL**.

## 1. Configuración del Entorno

### Crear carpeta del proyecto y entorno virtual
```powershell
# Crear carpeta del proyecto
mkdir Veterinaria
cd Veterinaria

# Configurar entorno virtual
python -m venv venv
.\venv\Scripts\activate

# Instalar dependencias
pip install django psycopg2-binary

# Generar requirements.txt
pip freeze > requirements.txt
```

## 2. Inicialización del Proyecto

### Crear proyecto y aplicación
```powershell
# Crear proyecto y aplicación
django-admin startproject clinica_veterinaria .
python manage.py startapp pacientes
```

## 3. Configuración de Base de Datos (PostgreSQL)

### En el motor de base de datos (psql/pgAdmin):
```sql
CREATE DATABASE clinica_veterinaria_db;
-- Nota: Se asume que el usuario 'neo' ya existe y tiene privilegios de superusuario.
```

### En `clinica_veterinaria/settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'pacientes',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'clinica_veterinaria_db',
        'USER': 'neo',
        'PASSWORD': 'su_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 4. Definición de Modelos (`pacientes/models.py`)

El sistema cuenta con dos entidades principales relacionadas:

```python
from django.db import models

class Propietario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50, null=True, blank=True)
    telefono_contacto = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

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
```

## 5. Gestión de Migraciones

Al ejecutar el comando de generación, Django crea archivos de migración en `pacientes/migrations/`.

### Archivo de Migración Inicial (`0001_initial.py`)
Este archivo traduce las clases de Python a operaciones de base de datos:

- **CreateModel**: Crea la tabla `pacientes_propietario`.
- **CreateModel**: Crea la tabla `pacientes_paciente` incluyendo la llave foránea (ForeignKey) hacia el propietario.

### Archivo de Migración Secundaria (`0002_propietario_apellido_propietario_email_and_more.py`)
Esta migración agrega campos adicionales al modelo Propietario y modifica el modelo Paciente:

- **AddField**: Agrega `apellido` y `email` a `pacientes_propietario`.
- **AlterField**: Modifica `fecha_nacimiento` en `pacientes_paciente` removiendo `help_text`.

### Comandos de Ejecución:
```powershell
# Generar los archivos de migración basados en los modelos
python manage.py makemigrations

# Aplicar las migraciones a la base de datos física
python manage.py migrate
```

## 6. Ejecución del Servidor

```powershell
python manage.py runserver
```

> **Nota**: Asegúrate de tener PostgreSQL instalado y configurado antes de ejecutar las migraciones.

## 7. Formularios (`pacientes/forms.py`)

Los formularios facilitan la validación y renderización de datos en los templates. Creamos un formulario basado en modelo para `Paciente`:

```python
from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'especie', 'raza', 'fecha_nacimiento', 'propietario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.Select(attrs={'class': 'form-control'}),
            'raza': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'propietario': forms.Select(attrs={'class': 'form-control'}),
        }
```

## 8. URLs y Vistas

### ¿Por qué Class-Based Views (CBV) en lugar de Function-Based Views (FBV)?

Como **principiante en Django**, es importante entender que Django ofrece dos formas principales de crear vistas:

- **Function-Based Views (FBV)**: Funciones simples que manejan una solicitud HTTP y devuelven una respuesta. Son más directas para principiantes pero pueden volverse repetitivas.
- **Class-Based Views (CBV)**: Clases que heredan de vistas genéricas de Django. Son más reutilizables, mantenibles y siguen el principio DRY (Don't Repeat Yourself).

**Usamos CBV porque:**
- ✅ **Menos código**: Django hace la mayor parte del trabajo
- ✅ **Reutilizable**: La misma clase puede usarse en múltiples lugares
- ✅ **Mantenible**: Fácil de extender y personalizar
- ✅ **Profesional**: Es el estándar en proyectos Django reales

### Configuración de URLs (`clinica_veterinaria/urls.py`):
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pacientes.urls')),  # Incluye las URLs de la app pacientes
]
```

### URLs de la aplicación (`pacientes/urls.py`):
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PacienteListView.as_view(), name='paciente_list'),           # Lista de pacientes
    path('nuevo/', views.PacienteCreateView.as_view(), name='paciente_create'),  # Crear paciente
    path('editar/<int:pk>/', views.PacienteUpdateView.as_view(), name='paciente_update'),  # Editar paciente
    path('eliminar/<int:pk>/', views.PacienteDeleteView.as_view(), name='paciente_delete'),  # Eliminar paciente
]
```

### Vistas basadas en clases (`pacientes/views.py`):

```python
from django.shortcuts import render
from .models import Paciente
from django.views.generic import ListView, CreateView, UpdateView, DeleteView  # Importamos las vistas genéricas
from django.urls import reverse_lazy  # Para redireccionar después de operaciones exitosas
from django.contrib import messages  # Para mostrar mensajes al usuario
from .forms import PacienteForm

# Vista para LISTAR pacientes (equivalente a SELECT *)
class PacienteListView(ListView):
    model = Paciente  # Modelo que queremos listar
    template_name = 'pacientes/paciente_list.html'  # Template a usar
    context_object_name = 'pacientes'  # Nombre de la variable en el template

# Vista para CREAR pacientes (equivalente a INSERT)
class PacienteCreateView(CreateView):
    model = Paciente  # Modelo a crear
    form_class = PacienteForm  # Formulario a usar
    template_name = 'pacientes/paciente_form.html'  # Template del formulario
    success_url = reverse_lazy('paciente_list')  # Redireccionar después de crear
    success_message = "Paciente creado exitosamente."  # Mensaje de éxito

# Vista para ACTUALIZAR pacientes (equivalente a UPDATE)
class PacienteUpdateView(UpdateView):
    model = Paciente  # Modelo a actualizar
    form_class = PacienteForm  # Formulario a usar
    template_name = 'pacientes/paciente_form.html'  # Template del formulario
    success_url = reverse_lazy('paciente_list')  # Redireccionar después de actualizar
    success_message = "Paciente actualizado exitosamente."  # Mensaje de éxito

# Vista para ELIMINAR pacientes (equivalente a DELETE)
class PacienteDeleteView(DeleteView):
    model = Paciente  # Modelo a eliminar
    template_name = 'pacientes/paciente_confirm_delete.html'  # Template de confirmación
    success_url = reverse_lazy('paciente_list')  # Redireccionar después de eliminar

    def form_valid(self, form):
        messages.success(self.request, "Paciente eliminado exitosamente.")
        return super().form_valid(form)
```

### 📚 **Guía paso a paso para principiantes - Cómo crear CBV:**

#### **Paso 1: Elegir la vista genérica correcta**
Django tiene vistas genéricas para operaciones comunes:
- `ListView` → Mostrar lista de objetos
- `DetailView` → Mostrar un objeto específico
- `CreateView` → Crear nuevos objetos
- `UpdateView` → Editar objetos existentes
- `DeleteView` → Eliminar objetos

#### **Paso 2: Configurar los atributos básicos**
Cada CBV necesita al menos:
- `model` → El modelo de Django a usar
- `template_name` → El archivo HTML que renderizará
- `success_url` → Dónde redirigir después de la operación

#### **Paso 3: Personalizar según necesites**
- `form_class` → Para CreateView/UpdateView (especifica el formulario)
- `context_object_name` → Nombre de la variable en el template
- `success_message` → Mensaje después de operación exitosa

#### **Paso 4: Conectar con URLs**
En `urls.py`, usa `.as_view()` para convertir la clase en vista:
```python
path('ruta/', MiVista.as_view(), name='nombre')
```

#### **Paso 5: Crear el template correspondiente**
Los templates siguen el patrón `app/model_accion.html` o puedes especificar con `template_name`.

### 🔄 **Comparación FBV vs CBV:**

| Operación | Function-Based View | Class-Based View |
|-----------|-------------------|------------------|
| **Crear** | 15-20 líneas de código | 5-8 líneas |
| **Listar** | 5-10 líneas | 3-4 líneas |
| **Editar** | 15-20 líneas | 5-8 líneas |
| **Eliminar** | 10-15 líneas | 4-6 líneas |

**CBV reduce el código en ~70% y es más mantenible.**

## 9. Templates

Django utiliza templates para separar la lógica de presentación. Creamos un directorio `templates/` en la raíz del proyecto con los siguientes archivos:

### Template base (`templates/base.html`):
```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Clínica Veterinaria</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
        <div class="container">
            <a class="navbar-brand" href="#">🐾 Clínica Veterinaria</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link text-white" href="#">Registrar Mascota</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <div class="container">
        {% block content %}
        <!-- Aqui se inyectara el contenido de las plantillas hijas -->
        {% endblock %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI"
        crossorigin="anonymous"></script>
</body>
</html>
```

### Lista de pacientes (`templates/pacientes/paciente_list.html`):
```html
{% extends 'base.html' %}

{% block content %}
<h2>Lista de Pacientes (mascotas)</h2>

<div class="card shadow-sm">
    <div class="card-body">
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Nombre</th>
                    <th>Especie</th>
                    <th>Raza</th>
                    <th>Fecha de Nacimiento</th>
                    <th>Propietario</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for paciente in pacientes %}
                <tr>
                    <td>{{ paciente.nombre }}</td>
                    <td>{{ paciente.especie }}</td>
                    <td>{{ paciente.raza }}</td>
                    <td>{{ paciente.fecha_nacimiento }}</td>
                    <td>{{ paciente.propietario }}</td>
                    <td>
                        <a href="{% url 'paciente_update' paciente.pk %}" class="btn btn-sm btn-primary">Editar</a>
                        <form action="{% url 'paciente_delete' paciente.pk %}" method="post" style="display:inline;">
                            {% csrf_token %}
                            <button type="submit" class="btn btn-sm btn-danger">Eliminar</button>
                        </form>
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="6" class="text-center">No hay pacientes registrados.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <a href="{% url 'paciente_create' %}" class="btn btn-primary">Nuevo Paciente</a>
    </div>
</div>
{% endblock %}
```

### Formulario de paciente (`templates/pacientes/paciente_form.html`):
```html
{% extends 'base.html' %}  <!-- Hereda del template base -->

{% block content %}
<div class="row justify-content-center">  <!-- Centra el formulario horizontalmente -->
    <div class="col-md-8">  <!-- Ancho responsivo: 8 columnas en medium+ -->
        <div class="card shadow-sm">  <!-- Tarjeta con sombra sutil -->
            <div class="card-header bg-primary text-white">  <!-- Cabecera azul con texto blanco -->
                <h5 class="mb-0">Registrar Nueva Mascota</h5>  <!-- Título del formulario -->
            </div>
            <div class="card-body">
                <form method="POST">  <!-- Formulario POST para enviar datos -->
                    {% csrf_token %}  <!-- Protección CSRF obligatoria -->

                    <!-- Renderiza todos los campos del formulario automáticamente -->
                    {{ form.as_p }}  <!-- 'as_p' = cada campo en un párrafo separado -->

                    <button type="submit" class="btn btn-success">Guardar</button>  <!-- Botón submit -->
                    <a href="{% url 'paciente_list' %}" class="btn btn-secondary">Cancelar</a>  <!-- Enlace cancelar -->
                </form>
            </div>
        </div>
    </div>
{% endblock %}
```

### 📚 **Explicación de los templates:**

Los templates utilizan una estructura de tabla para la lista de pacientes, lo que facilita la comparación de datos. La eliminación se realiza directamente desde la tabla mediante formularios inline para una experiencia más fluida.

### Confirmación de eliminación (`templates/pacientes/paciente_confirm_delte.html`):

**Nota**: Este archivo está vacío en la implementación actual. La eliminación de pacientes se realiza directamente desde la tabla en `paciente_list.html` mediante un formulario inline, sin necesidad de una página de confirmación separada.

## 10. Panel de Administración

### Registro de modelos en el admin (`pacientes/admin.py`):
```python
from django.contrib import admin
from .models import Propietario, Paciente

@admin.register(Propietario)
class PropietarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono_contacto')
    search_fields = ('nombre', 'telefono_contacto')

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'raza', 'fecha_nacimiento', 'fecha_registro', 'propietario')
    list_filter = ('especie', 'fecha_registro')
    search_fields = ('nombre', 'raza', 'propietario__nombre')
```

### Creación del superusuario:
```powershell
python manage.py createsuperuser
```

## 11. Resumen del Proyecto

### Tecnologías Utilizadas:
- **Backend**: Django 6.0.3 (Python web framework)
- **Base de Datos**: PostgreSQL
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Arquitectura**: MTV (Model-Template-View)

### Funcionalidades Implementadas:
- ✅ Gestión completa de propietarios
- ✅ Gestión completa de pacientes (CRUD)
- ✅ Interfaz web responsiva con Bootstrap
- ✅ Panel de administración de Django
- ✅ Validación de formularios
- ✅ Relaciones entre modelos
- ✅ Migraciones de base de datos

### Estructura del Proyecto:
```
Veterinaria/
├── clinica_veterinaria/          # Configuración del proyecto
│   ├── settings.py              # Configuración principal
│   ├── urls.py                  # URLs del proyecto
│   └── ...
├── pacientes/                   # Aplicación principal
│   ├── models.py                # Modelos de datos
│   ├── views.py                 # Lógica de vistas
│   ├── forms.py                 # Formularios
│   ├── admin.py                 # Configuración del admin
│   └── ...
├── templates/                   # Templates HTML
│   ├── base.html
│   ├── pacientes/
│   │   ├── paciente_list.html
│   │   ├── paciente_form.html
│   │   └── paciente_confirm_delte.html
├── manage.py                    # Script de gestión
├── requirements.txt             # Dependencias: asgiref, Django, psycopg2-binary, sqlparse, tzdata
└── README.md                    # Este archivo
```

### Próximos Pasos:
- Implementar autenticación de usuarios
- Agregar más funcionalidades (citas, tratamientos, etc.)
- Mejorar el diseño de la interfaz
- Agregar tests unitarios
- Desplegar en producción

---

**Desarrollado por**: Neo
**Fecha**: 20 de marzo de 2026
**Versión**: 1.0.0