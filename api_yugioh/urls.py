from django.urls import path
from . import views

urlpatterns = [
    path('cards/', views.get_card, name='get_card'),
    path('search/', views.search_card, name='search_card'),
]   