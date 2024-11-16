import requests
import random
from django.shortcuts import render, redirect
from requests.exceptions import RequestException
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import UsuarioForm

api_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
def get_cards_from_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si el código de estado es 4xx o 5xx
        return response.json().get('data', [])
    except RequestException as e:
        print(f'Error al hacer la solicitud a la API: {e}')
        return []

def card_info_view(request):
    cards = get_cards_from_api(api_url)
    
    if cards:
        random_cards = random.sample(cards, 40)
        context = {'cards': random_cards}
    else:
        context = {'error': 'No se pudieron obtener las cartas de la API'}

    return render(request, 'cards_info_views.html', context)

def home(request):
    return render(request, 'index.html')

def card_info(request, card_name):
    return render(request, 'card_info.html', {'card_name': card_name})

def search_cards(request):
    query = request.GET.get('q')
    cards = []
    
    if query:
        # Limpieza básica del input
        query = query.strip()
        
        if query:
            api_query_url = f'{api_url}?name={query}'
            cards = get_cards_from_api(api_query_url)

    context = {'cards': cards, 'query': query}
    return render(request, 'search_card.html', context)

def random_card(request):
    
    cards = get_cards_from_api(api_url)
    
    # Filtrar cartas que sean del tipo "Effect Monster"
    effect_monsters = [card for card in cards if card['type'] == "Effect Monster"]
    
    # Seleccionar una carta monstruo de efecto aleatoria
    if effect_monsters:
        random_card = random.choice(effect_monsters)
        context = {'card': random_card}
    else:
        context = {'error': 'No se encontraron cartas del tipo "Effect Monster" o no se pudieron obtener las cartas de la API'}
    
    return render(request, 'random_card.html', context)

def login_user(request):  # noqa: F811
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'Username or Password is incorrect.'
            })
        else:
            login(request, user)
            return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST) 
        if form.is_valid():
            try:
                form.save()  # Intenta guardar los datos en la base de datos
                return redirect('login_user')  # Redirige después de guardar el usuario

            except IntegrityError:
                # Este error se lanzará si hay un valor duplicado en un campo único
                #error = "El usuario o correo ya existe. Intenta con uno diferente."
                error = "IntegrityError"
                return render(request, 'signup.html', {'form': form, 'error': error})

        else:
            #error = "Formulario inválido. Verifica los datos ingresados."
            error = "else"
            return render(request, 'signup.html', {'form': form, 'error': error})

    else:
        form = UsuarioForm()  # Muestra el formulario vacío para un GET request
        return render(request, 'signup.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('home')