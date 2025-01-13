import requests
import random
from django.shortcuts import render, redirect
from requests.exceptions import RequestException
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login

from api_yugioh.models import Card
from .forms import UserRegistrationForm
from django.contrib import messages
from django.core.paginator import Paginator
from .models import CustomUser

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
    query = request.GET.get('q')  # Obtener el parámetro de búsqueda si existe
    cards = []
    
    if query:  # Si hay un término de búsqueda
        # Limpieza básica del input
        query = query.strip()
        if query:
            api_query_url = f'{api_url}?name={query}'
            cards = get_cards_from_api(api_query_url)
    else:  # Si no hay búsqueda, mostrar cartas al azar
        cards = get_cards_from_api(api_url)
        if cards:
            random_cards = random.sample(cards, 20)
            # Guardar cartas en la base de datos
            for card in random_cards:
                card_image = card['card_images'][0]['image_url']  # Obtener la URL de la imagen principal
                Card.objects.get_or_create(
                    name=card['name'],
                    defaults={
                        'image_url': card_image,
                        'description': card.get('desc', '')  # Asegúrate de usar la clave correcta para la descripción
                    }
                )
            cards = random_cards

    context = {
        'cards': cards,
        'query': query,  # Incluir el término de búsqueda en el contexto
    }
    
    return render(request, 'cards_info_views.html', context)


def saved_cards_view(request): 
    cards = Card.objects.all().order_by('-searched_at')  # Orden por fecha de búsqueda
    paginator = Paginator(cards, 10)  # 10 cartas por página

    page_number = request.GET.get('page')
    page_cards = paginator.get_page(page_number)

    context = {'cards': page_cards}  # Cambiado a 'cards' para coincidir con la plantilla
    return render(request, 'saved_cards.html', context)

def search_cards(request):
    cards = get_cards_from_api(api_url)
    query = request.GET.get('q')
    cards = []
    
    if query:
        # Limpieza básica del input
        query = query.strip()
        
        if query:
            api_query_url = f'{api_url}?name={query}'
            cards = get_cards_from_api(api_query_url)

    context = {'cards': cards, 'query': query}
    return render(request, 'search_cards.html', context)

def card_search(request):
    query = request.GET.get('q', '').strip()  # Obtener y limpiar el parámetro de búsqueda
    cards = []

    if query:
        # Construir la URL de búsqueda con el término ingresado
        api_query_url = f'{api_url}?name={query}'
        try:
            response = requests.get(api_query_url)
            if response.status_code == 200:
                cards = response.json().get('data', [])  # Asumiendo que devuelve una lista de cartas
            else:
                print(f"Error al consultar la API: {response.status_code}")
        except requests.RequestException as e:
            print(f"Excepción al consultar la API: {e}")

    context = {
        'cards': cards,
        'query': query,
    }

    print(context)
    return render(request, 'search_cards.html', context)

def home_or_search(request):
    query = request.GET.get('q')  # Obtener el parámetro de búsqueda si existe
    cards = []
    
    if query:  # Si hay un término de búsqueda
        # Limpieza básica del input
        query = query.strip()
        if query:
            api_query_url = f'{api_url}?name={query}'
            cards = get_cards_from_api(api_query_url)
    else:  # Si no hay búsqueda, mostrar cartas al azar
        cards = get_cards_from_api(api_url)
        if cards:
            random_cards = random.sample(cards, 20)
            # Guardar cartas en la base de datos
            for card in random_cards:
                card_image = card['card_images'][0]['image_url']  # Obtener la URL de la imagen principal
                Card.objects.get_or_create(
                    name=card['name'],
                    defaults={
                        'image_url': card_image,
                        'description': card.get('desc', '')  # Asegúrate de usar la clave correcta para la descripción
                    }
                )
            cards = random_cards

    context = {
        'cards': cards,
        'query': query,  # Incluir el término de búsqueda en el contexto
    }
    
    return render(request, 'index.html', context)


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

def login_user(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verificar si el usuario existe
        try:
            user_exists = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Usuario no registrado.')
            return redirect('login')

        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Si las credenciales son válidas, inicia sesión
            auth_login(request, user)
            messages.success(request, f'Bienvenido, {username}.')
            return redirect('home')  # Redirige a la página principal
        else:
            # Si las credenciales no son válidas
            messages.error(request, 'Contraseña incorrecta.')
            return redirect('login')
    else:
        # Renderizar el formulario de login
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect('login')
        else:
            messages.error(request, "Por favor, corrige los errores del formulario.")
            # Imprime el error para debug
            print(form.errors)  # Esto te ayudará a ver el problema directamente
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('home')


def search_cards_view(request):
    #Obtén los parámetros de búsqueda desde la solicitud
    name = request.GET.get('name', '')
    card_type = request.GET.get('type', '')
    archetype = request.GET.get('archetype', '')
    set_name = request.GET.get('set_name', '')
    set_rarity = request.GET.get('set_rarity', '')

    #Construir filtros para la API
    params = {}
    if name:
        params['fname'] = name
    if card_type:
        params['type'] = card_type
    if archetype:
        params['archetype'] = archetype
    if set_name:
        params['set'] = set_name
    if set_rarity:
        params['rarity'] = set_rarity

    #Obtener datos de la API
    url_with_params = api_url
    if params:
        url_with_params = f"{api_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

    cards = get_cards_from_api(url_with_params)

    context = {'cards': cards}
    return render(request, 'search_results.html', context)  