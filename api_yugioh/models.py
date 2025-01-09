from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .validator import validate_password_strength

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Email único
    username = models.CharField(max_length=100, unique=True)  # Username único

    # Sobrescribir el campo de password si es necesario
    # password = models.CharField(max_length=128)

    REQUIRED_FIELDS = ['email']  # Email es obligatorio junto con el username
    USERNAME_FIELD = 'username'  # Username será el identificador único

    def __str__(self):
        return self.username

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