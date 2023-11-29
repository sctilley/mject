from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('decks/', views.decks, name='decks'),
    path('test/', views.test, name='test'),
]