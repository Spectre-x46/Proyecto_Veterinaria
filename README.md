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
    telefono_contacto = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} - {self.telefono_contacto}"

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
    fecha_nacimiento = models.DateField(help_text="Fecha de nacimiento de la mascota")
    fecha_registro = models.DateField(auto_now_add=True)
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='pacientes')
```

## 5. Gestión de Migraciones

Al ejecutar el comando de generación, Django crea el archivo `pacientes/migrations/0001_initial.py`, el cual contiene las instrucciones técnicas para crear las tablas en PostgreSQL.

### Archivo de Migración Inicial (`0001_initial.py`)
Este archivo traduce las clases de Python a operaciones de base de datos:

- **CreateModel**: Crea la tabla `pacientes_propietario`.
- **CreateModel**: Crea la tabla `pacientes_paciente` incluyendo la llave foránea (ForeignKey) hacia el propietario.

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