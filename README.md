# Inta_Code: Legacy Code Assistant (VB6 to C++)

Este proyecto es un asistente inteligente diseñado para facilitar la transición de sistemas legados escritos en **Visual Basic 6** hacia **C++ moderno**, utilizando modelos de lenguaje de última generación (Gemini 2.5 Flash).

## Preparación del Entorno

Sigue estos pasos para replicar el entorno de desarrollo y ejecución:

### 1. Clonación y Estructura
Asegúrate de estar en la carpeta raíz del proyecto `Insta_Code`.

### 2. Entorno Virtual (venv)
Es obligatorio el uso de un entorno virtual para aislar las dependencias:
```powershell
# Creación del entorno
python -m venv venv

# Activación en PowerShell
.\venv\Scripts\activate

### 3. Instalaccion de requisitos

pip install django djangorestframework django-cors-headers google-genai

## para comprobar su comunicacion

python test_ia.py


