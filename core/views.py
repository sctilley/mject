from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse 
from django import forms
from django.forms import modelform_factory
# from .models import Deck, League, Match, Flavor, MtgFormat, Archetype
# from .forms import DeckForm, LeagueForm, MatchForm, FlavorForm, TestForm
from django.db.models.functions import Lower
from django.db.models import Count, Q

def home(request):
    user = request.user
        
    context = {

    }
    return render(request, "core/home.html", context)

def test(request):

    context = {

    }

    return render(request, "core/test.html", context)

@login_required
def decks(request):

    context = {
    }

    return render(request, 'core/decks.html', context)