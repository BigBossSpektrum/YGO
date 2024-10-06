#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yugioh_page_main.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Obtenemos el puerto desde la variable de entorno o usamos 4000 como predeterminado
    port = os.environ.get("PORT", "4000")

    # Ejecutamos el comando para correr el servidor en el puerto asignado
    execute_from_command_line(sys.argv + ["runserver", f"0.0.0.0:{port}"])

if __name__ == '__main__':
    main()
