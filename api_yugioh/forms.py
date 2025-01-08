from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from api_yugioh.models import CustomUser
from .validator import validate_password_strength

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        help_text="La contraseña debe incluir al menos una mayúscula, un número y un símbolo especial.",
        required=True,
        validators=[validate_password_strength]
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput(),
        required=True
    )

    class Meta:
        model = CustomUser  # Cambia 'User' por 'CustomUser'
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k: "" for k in fields}  # Esto desactiva los textos de ayuda predeterminados
