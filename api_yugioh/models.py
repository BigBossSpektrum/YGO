from django.db import models
from django.contrib.auth.models import AbstractUser, User
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
    """
    Modelo para representar las cartas obtenidas de la API.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    card_type = models.CharField(max_length=50, blank=True, null=True)  # Tipo de carta (e.g., Monster, Spell)
    archetype = models.CharField(max_length=100, blank=True, null=True)
    rarity = models.CharField(max_length=50, blank=True, null=True)
    race = models.CharField(max_length=50, blank=True, null=True)
    attribute = models.CharField(max_length=50, blank=True, null=True)  # Atributo (e.g., DARK, LIGHT)
    humanReadableCardType = models.CharField(max_length=50, blank=True, null=True)
    atk = models.IntegerField(blank=True, null=True, default=0)  # Ataque
    defense = models.IntegerField(blank=True, null=True, default=0)  # Defensa
    level = models.IntegerField(blank=True, null=True)  # Nivel/Estrellas
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Precio de la carta
    image_url = models.URLField(blank=True, null=True)  # URL de la imagen de la carta

    def __str__(self):
        return self.name

class Cart(models.Model):
    """
    Modelo para representar el carrito de un usuario.
    """
    CustomUser = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.CustomUser.username}"

    def total_price(self):
        """
        Calcula el precio total de las cartas en el carrito.
        """
        return sum(item.total_price() for item in self.cartitems.all())

class CartItem(models.Model):
    """
    Modelo para representar un ítem en el carrito de compras.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartitems")
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.card.name}"

    def total_price(self):
        """
        Calcula el precio total para esta cantidad de cartas.
        """
        return self.card.price * self.quantity

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Sell(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.URLField()
    condition = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
class Order(models.Model):
    """
    Modelo para representar una orden de compra.
    """
    CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Orden #{self.id} de {self.CustomUser.username}"

class OrderItem(models.Model):
    """
    Modelo para representar los ítems dentro de una orden de compra.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitems")
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.card.name}"

    def total_price(self):
        """
        Calcula el precio total para esta cantidad de cartas.
        """
        return self.card.price * self.quantity