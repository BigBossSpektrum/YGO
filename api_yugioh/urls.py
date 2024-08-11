from django.urls import path
from . import views

urlpatterns = [
    path('cards/', views.get_cards, name='get_cards'),
    path('search/', views.search_card, name='search_card'),
]   