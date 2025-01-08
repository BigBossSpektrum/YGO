from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .validator import validate_password_strength

# Create your models here.

class Usuarios(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)

    ultimo_login = models.DateTimeField(auto_now=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado_activo = models.BooleanField(default=True)

class CustomUser(AbstractUser):
    password1 = models.CharField(
        max_length=128,
        validators=[validate_password_strength],
        help_text="La contraseña debe incluir al menos una mayúscula, un número y un símbolo especial."
    )

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Cambia el nombre relacionado
        blank=True,
        help_text="Los grupos a los que pertenece este usuario.",
        verbose_name="grupos"
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",  # Cambia el nombre relacionado
        blank=True,
        help_text="Permisos específicos para este usuario.",
        verbose_name="permisos de usuario"
    )

class CardSet(models.Model):
    card = models.ForeignKey('Card', on_delete=models.CASCADE, related_name='card_sets')
    set_name = models.CharField(max_length=255)
    set_rarity = models.CharField(max_length=100)
    set_price = models.DecimalField(max_digits=10, decimal_places=2)

class Card(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, default="Unknown")
    archetype = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    searched_at = models.DateTimeField(auto_now_add=True)