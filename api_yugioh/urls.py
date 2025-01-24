from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # path('card/', views.get_card, name='get_card'),
    # path('card/<str:card_name>/', views.get_card, name='get_card'),
    # path('search/', views.search_card, name='search_card'),
    path('', views.home_or_search, name='home'),
    path('cards_info/', views.card_info_view, name='card_info_view'),
    path('random_card/', views.random_card, name='random_card'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('signup/', views.register, name='signup'),
    path('search_cards/', views.search_cards, name='search_cards'),
    path('search', views.card_search, name='search'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile_view, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:card_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.order_success, name='order_success'),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)