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
        return render(request, 'base.html', context)
    else:
        # En caso de error, puedes manejarlo aquí
        return render(request, 'base.html', {'error': 'No se pudieron obtener las cartas de la API'})
