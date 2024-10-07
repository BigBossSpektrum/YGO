import requests
import random
from django.shortcuts import render

api_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
# api_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Decode%20Talker'


def card_info_view(request):
    
    # Realizar la solicitud a la API
    response = requests.get(api_url)
    
    if response.status_code == 200:
        # Si la solicitud es exitosa, obtenemos las cartas
        cards = response.json()['data']
        
        # Selecciona 50 cartas al azar
        random_cards = random.sample(cards, 40)
        
        # Pasar las cartas a la plantilla
        context = {'cards': random_cards}
        return render(request, 'base_main.html', context)
    else:
        # En caso de error, puedes manejarlo aquí
        return render(request, 'base_main.html', {'error': 'No se pudieron obtener las cartas de la API'})


def home(request):
    return render(request, 'index.html')

def card_info(request, card_name):
    return render(request, 'card_info.html', {'card_name': card_name})

def search_cards(request):
    query = request.GET.get('q')
    cards = []
    if query:
        response = requests.get(f'{api_url}?name={query}')
        cards = response.json().get('data', [])
    return render(request, 'search_card.html', {'cards': cards, 'query': query})

def random_card(request):
    response = requests.get(api_url)

    if response.status_code == 200:
        cards = response.json()['data']

    random_card = random.choice(cards)
    context = {'card': random_card}

    return render(request, 'random_card.html', context)

