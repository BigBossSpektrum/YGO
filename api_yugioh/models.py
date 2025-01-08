from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .validator import validate_password_strength

# Create your models here.

class CustomUser(AbstractUser):
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

    # Asegúrate de que el validador personalizado se aplica al campo de contraseña
    password = models.CharField(
        max_length=128,  # Longitud del campo de contraseña
        validators=[validate_password_strength],  # Aquí estamos aplicando el validador personalizado
        help_text="La contraseña debe incluir al menos una mayúscula, un número y un símbolo especial."
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