from django.db import models

# Create your models here.

class Usuarios(models.Model):
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)

    ultimo_login = models.DateTimeField(auto_now=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado_activo = models.BooleanField(default=True)
    J