from django.db import models

# Create your models here.

class Usuarios(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)

    ultimo_login = models.DateTimeField(auto_now=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado_activo = models.BooleanField(default=True)


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