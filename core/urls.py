from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('decks/', views.decks, name='decks'),
    path('test/', views.test, name='test'),
]


#leagues
urlpatterns += [
    path('add_league', views.add_league, name='add_league'),

]

#decks
urlpatterns += [
    path('add_deck', views.add_deck, name='add_deck'),
    path('submit_new_deck', views.submit_new_deck, name='submit_new_deck'),
    path('cancel_add_deck', views.cancel_add_deck, name='cancel_add_deck'),
    path('<int:deck_pk>/delete_deck', views.delete_deck, name='delete_deck'),
    path('<int:deck_pk>/edit_deck', views.edit_deck, name='edit_deck'),
    path('<int:deck_pk>/edit_deck_submit', views.edit_deck_submit, name='edit_deck_submit'),
    path('decks_table', views.decks_table, name='decks_table'),
    path('<int:deck_pk>/add_varient', views.add_varient, name='add_varient'),
    path('submit_new_flavor', views.submit_new_flavor, name='submit_new_flavor'),
    path('<int:flavor_pk>/delete_flavor', views.delete_flavor, name='delete_flavor'),
    path('<int:flavor_pk>/edit_flavor', views.edit_flavor, name='edit_flavor'),
    path('<int:flavor_pk>/edit_flavor_submit', views.edit_flavor_submit, name='edit_flavor_submit'),
]