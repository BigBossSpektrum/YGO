import requests
import random
from django.shortcuts import render, redirect, get_object_or_404
from requests.exceptions import RequestException
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from api_yugioh.models import Card
from .forms import UserRegistrationForm, CheckoutForm
from django.contrib import messages
from django.core.paginator import Paginator
from .models import CustomUser, Cart, Order, OrderItem, CartItem

api_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
def get_cards_from_api(url):
    try:
        response = requests.get(url)
        # print("Estado de la API:", response.status_code)
        # print("Respuesta de la API:", response.json())
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
    
    return render(request, 'page/cards_info_views.html', context)
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
    cards = []

    # Obtener los parámetros del filtro desde la solicitud (GET)
    query = request.GET.get('q', '').strip()  # Filtro por nombre de carta
    min_atk = request.GET.get('min_atk')  # Rango mínimo de ataque
    max_atk = request.GET.get('max_atk')  # Rango máximo de ataque
    min_def = request.GET.get('min_def')  # Rango mínimo de defensa
    max_def = request.GET.get('max_def')  # Rango máximo de defensa
    card_types = request.GET.getlist('type')  # Lista de tipos seleccionados
    attributes = request.GET.getlist('attribute')  # Lista de atributos seleccionados
    archetype = request.GET.get('archetype', '').strip()  # Filtro por arquetipo
    min_stars = request.GET.get('min_stars')  # Rango mínimo de estrellas
    max_stars = request.GET.get('max_stars')  # Rango máximo de estrellas
    rarity = request.GET.get('rarity', '').strip()  # Filtro por rareza

    try:
        # Llamar a la API y obtener todas las cartas
        response = requests.get(api_url)
        if response.status_code == 200:
            all_cards = response.json()

            # Filtro por nombre de carta (si se especificó en la búsqueda)
            if query:
                all_cards = [card for card in all_cards if query.lower() in card['name'].lower()]

            # Filtro por rango de ataque
            if min_atk:
                all_cards = [card for card in all_cards if card.get('atk') and int(card['atk']) >= int(min_atk)]
            if max_atk:
                all_cards = [card for card in all_cards if card.get('atk') and int(card['atk']) <= int(max_atk)]

            # Filtro por rango de defensa
            if min_def:
                all_cards = [card for card in all_cards if card.get('def') and int(card['def']) >= int(min_def)]
            if max_def:
                all_cards = [card for card in all_cards if card.get('def') and int(card['def']) <= int(max_def)]

            # Filtro por tipos seleccionados
            if card_types:
                all_cards = [card for card in all_cards if card.get('type') in card_types]

            # Filtro por atributos seleccionados
            if attributes:
                all_cards = [card for card in all_cards if card.get('attribute') in attributes]

            # Filtro por arquetipo
            if archetype:
                all_cards = [card for card in all_cards if card.get('archetype') and archetype.lower() in card['archetype'].lower()]

            # Filtro por rango de estrellas
            if min_stars:
                all_cards = [card for card in all_cards if card.get('level') and int(card['level']) >= int(min_stars)]
            if max_stars:
                all_cards = [card for card in all_cards if card.get('level') and int(card['level']) <= int(max_stars)]

            # Filtro por rareza
            if rarity:
                all_cards = [card for card in all_cards if any(rarity.lower() in set.get('set_rarity', '').lower() for set in card.get('card_sets', []))]

            # Asignar las cartas filtradas
            cards = all_cards

    except Exception as e:
        print(f"Error al obtener datos de la API: {e}")

    # Pasar los filtros y las cartas encontradas al contexto para el template
    context = {
        'cards': cards,
        'query': query,
        'min_atk': min_atk,
        'max_atk': max_atk,
        'min_def': min_def,
        'max_def': max_def,
        'card_types': card_types,
        'attributes': attributes,
        'archetype': archetype,
        'min_stars': min_stars,
        'max_stars': max_stars,
        'rarity': rarity,
    }
 
    return render(request, 'partials_results.html', context)
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
    
    return render(request, 'page/index.html', context)
def random_card(request):
    # Lista de tipos de cartas
    card_types = ["Monster", "Spell", "Trap"]
    
    # Seleccionar aleatoriamente un tipo de carta
    selected_type = random.choice(card_types)
    
    # Obtener todas las cartas desde la API
    cards = get_cards_from_api(api_url)
    
    # Filtrar las cartas basadas en el tipo seleccionado
    filtered_cards = []
    if selected_type == "Monster":
        filtered_cards = [card for card in cards if "Monster" in card['type']]
    elif selected_type == "Spell":
        filtered_cards = [card for card in cards if "Spell" in card['type']]
    elif selected_type == "Trap":
        filtered_cards = [card for card in cards if "Trap" in card['type']]
    
    # Seleccionar una carta aleatoria del tipo seleccionado
    if filtered_cards:
        random_card = random.choice(filtered_cards)
        context = {'card': random_card, 'type': selected_type}
    else:
        context = {
            'error': f'No se encontraron cartas del tipo "{selected_type}" o no se pudieron obtener las cartas de la API.',
            'type': selected_type,
        }
    
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
        return render(request, 'user/login.html', {'form': form})
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

    return render(request, 'user/register.html', {'form': form})
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
@login_required
def profile_view(request):
    return render(request, 'user/profile.html', {'user': request.user})
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # Actualiza la sesión del usuario para que siga autenticado
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Tu contraseña ha sido cambiada exitosamente.')
            return redirect('profile')  # Redirigir al perfil después de cambiar la contraseña
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'page/change_password.html', {'form': form})
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('profile')  # Redirigir al perfil después de editarlo
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'user/edit_profile.html', {'form': form})

def checkout(request):
    # Obtener o crear el carrito del usuario
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Crear un pedido
            order = Order.objects.create(
                user=request.user,
                is_paid=False,
                total_price=cart.total_price()
            )
            # Agregar ítems del carrito al pedido
            for item in cart.cartitems.all():
                OrderItem.objects.create(
                    order=order,
                    card=item.card,
                    quantity=item.quantity
                )
            # Limpiar el carrito después de crear el pedido
            cart.cartitems.all().delete()
            return redirect('order_success')  # Redirigir a una página de éxito
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form, 'cart': cart})

def order_success(request):
    return render(request, 'order_success.html')

def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})

def add_to_cart(request, card_id):
    card = get_object_or_404(get_cards_from_api(api_url), id=card_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, card=card)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('view_cart')

