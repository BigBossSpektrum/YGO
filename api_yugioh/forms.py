# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Order, CartItem
from django.core.exceptions import ValidationError

# Validador para contraseña
def validate_password_strength(value):
    if len(value) < 8:
        raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
    if not any(char in "!@#$%^&*()_+[]{}|;:,.<>?/" for char in value):
        raise ValidationError("La contraseña debe incluir al menos un carácter especial.")

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(),
        validators=[validate_password_strength],  # Agregamos el validador personalizado
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput()
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

class OrderForm(forms.ModelForm):
    """
    Formulario para crear o actualizar pedidos.
    """
    class Meta:
        model = Order
        fields = ['is_paid']
        labels = {
            'is_paid': '¿Pagado?',
        }
        widgets = {
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CartItemForm(forms.ModelForm):
    """
    Formulario para agregar o actualizar ítems en el carrito.
    """
    class Meta:
        model = CartItem
        fields = ['card', 'quantity']
        labels = {
            'card': 'Carta',
            'quantity': 'Cantidad',
        }
        widgets = {
            'card': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class CheckoutForm(forms.Form):
    """
    Formulario de checkout para recopilar datos del cliente al procesar el pedido.
    """
    full_name = forms.CharField(
        max_length=255,
        label="Nombre completo",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo'}),
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu correo electrónico'}),
    )
    phone_number = forms.CharField(
        max_length=15,
        label="Número de teléfono",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu número de teléfono'}),
    )
    address = forms.CharField(
        max_length=255,
        label="Dirección de entrega",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu dirección de entrega'}),
    )
    city = forms.CharField(
        max_length=100,
        label="Ciudad",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu ciudad'}),
    )
    zip_code = forms.CharField(
        max_length=10,
        label="Código postal",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu código postal'}),
    )

