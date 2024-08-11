import requests
import random
from django.shortcuts import render

api_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
# api_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Decode%20Talker'

def get_cards(request):
    response = requests.get(api_url)
    data = response.json()

    cards = random.sample(data['data'], 50) #obtener solo los primeros 10 elementos
    return render (request, 'cards_info.html', {'cards': cards})

def search_card(request):
    query = request.GET.get('q')
    cards = []
    if query:
        response = requests.get(f'{api_url}?name={query}')
        cards = response.json().get('data', [])
    return render(request, 'cards_info.html', {'cards': cards, 'query': query})
