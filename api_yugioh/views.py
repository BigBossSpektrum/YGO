import requests
import random
from django.shortcuts import render

api_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
# api_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Decode%20Talker'

def card_info_view(request):
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        cards = random.sample(data['data'], 50)  # Aquí obtienes la lista de cartas de la API
    else:
        cards = []  # En caso de que haya un error en la API

    return render(request, 'base.html', {'cards': cards})



# def get_cards(request):
#     response = requests.get(api_url)
#     data = response.json()

#     cards = random.sample(data['data'], 50) #obtener solo los primeros 10 elementos
#     return render (request, 'cards_info.html', {'cards': cards})

# def get_card(request, card_name):
#     response = requests.get(f'{api_url}?name={card_name}')
#     card = response.json().get('data', [])[0]
#     return render(request, 'card_info.html', {'card': card})

# def get_card_random(request, random='data=random'):
#     response = requests.get(f'{api_url}?{random}')
#     card = response.json().get('data', [])[0]
#     card_image_url = card.get('card_images', [])[0].get('image_url')
#     return render(request, './templates/base.html', {'card': card, 'card_image_url': card_image_url})

# def search_card(request):
#     query = request.GET.get('q')
#     response = requests.get(f'{api_url}?name={query}')
#     cards = response.json().get('data', [])
#     return render(request, 'search.html', {'cards': cards})

