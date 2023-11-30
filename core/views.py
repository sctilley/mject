from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse 
from django import forms
from django.forms import modelform_factory
from .models import Deck, Flavor, MtgFormat, Archetype
from .forms import DeckForm, FlavorForm, LeagueForm
from django.db.models.functions import Lower
from django.db.models import Count, Q

from users.models import CustomUser

def home(request):
    user = request.user
    lform = LeagueForm()

    if request.method == 'POST':
        print("request.post trigger", request.POST)
        lform = LeagueForm(request.POST)
        if lform.is_valid():
            new_league = lform.save(commit=False)
            new_league.user = request.user
            new_league.save()

            user.profile.recentFormat = new_league.mtgFormat
            user.profile.recentDeck = new_league.myDeck
            user.profile.save()

            newleague = League.objects.latest('dateCreated')
            print("new league: ", newleague)

            for i in range(1,6):
                Match.objects.create(
                    league_id=new_league.pk,
                    user=user,
                    mtgFormat=new_league.mtgFormat,
                    myDeck=new_league.myDeck,
                    inLeagueNum=i,
                    didjawin=None
                )


        else:
            print("errors: ", lform.errors)
    context = {

    }
    return render(request, "core/home.html", context)

def test(request):

    context = {

    }

    return render(request, "core/test.html", context)

#leagues
def add_league(request):
    try:
        current_league = League.objects.filter(user=request.user).latest('dateCreated')
    except:
        current_league = League.objects.none()

    if current_league.isFinished == True:
        context = {
            'lform':LeagueForm()
        }
    else:
        context = {

        }


    return render(request, 'core/partials/add_league.html', context)

# decks 
@login_required
def decks(request):
    decks_list = Deck.objects.all().order_by('-dateCreated')
    context = {
        "decks": decks_list
    }
    return render(request, 'core/decks.html', context)


def decks_table(request):
    decks_list = Deck.objects.all().order_by('-dateCreated')
    context = {
        "decks": decks_list
    }
    return render(request, 'core/partials/decks/decks_table.html', context)

def add_deck(request):
    context = {
        'form':DeckForm()
    }
    return render(request, 'core/partials/decks/add_deck.html', context)

def delete_deck(request, deck_pk):
    deck = Deck.objects.get(pk=deck_pk)
    deck.delete()
    return HttpResponse()

def edit_deck(request, deck_pk):
    deck = Deck.objects.get(pk=deck_pk)
    context = {}
    context['deck'] = deck
    context['form'] = DeckForm(initial={
        'name':deck.name,
        'mtgFormat': deck.mtgFormat,
        'archetype': deck.archetype,
    })
    return render(request, 'core/partials/decks/edit_deck.html', context)

def edit_deck_submit(request, deck_pk):
    context = {}
    deck = Deck.objects.get(pk=deck_pk)
    context['deck'] = deck
    if request.method == 'POST':
        form = DeckForm(request.POST, instance=deck)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'core/partials/decks/edit_deck.html', context)
        
    return render(request, 'core/partials/decks/deck_row.html', context)

def submit_new_deck(request):
    form = DeckForm(request.POST)
    print("deck form request.post: ", request.POST)
    context = {
        'form':form
    }

    if form.is_valid():
        newdeck = form.save()
        newflavorname = request.POST['flavorname']
        if newflavorname:
            Flavor.objects.create(
                    deck_id=newdeck.pk,
                    name = "none"
                )
            if 'fisdefault' in request.POST:
                Flavor.objects.create(
                    deck_id=newdeck.pk,
                    name = newflavorname,
                    isdefault = True
                )
            else:
                Flavor.objects.create(
                    deck_id=newdeck.pk,
                    name = newflavorname
                )
        else:
            Flavor.objects.create(
                    deck_id=newdeck.pk,
                    name = "none"
                )

    else:
        print("form error")
        return render(request, 'core/partials/decks/add_deck.html', context)
    context = {
        'form':form,
        'deck':newdeck
    }
    return render(request, 'core/partials/decks/deck_row.html', context)

def cancel_add_deck(request):
    return HttpResponse()

    
def add_varient(request, deck_pk):
    print("add varient")
    context = {
        'form':FlavorForm(initial={'deck': deck_pk})
    }
    return render(request, 'core/partials/decks/add_flavor.html', context)

def submit_new_flavor(request):
    form = FlavorForm(request.POST)
    context = {
        'form':form
    }

    if form.is_valid():
        new_flavor = form.save(commit=False)
        if new_flavor.isdefault == True:
            print("to do logic")
            Flavor.objects.all().update(isdefault=False)
            new_flavor.save()
        else:
            new_flavor.save()

        affecteddeck = Deck.objects.get(id=new_flavor.deck.id)
            
        print("affecteddeck: ", affecteddeck)
        newflavorsdecksflavors = Flavor.objects.filter()
        context['flavor'] = new_flavor
    else:
        print("form error")
        return render(request, 'core/partials/decks/new_varient.html', context)
    return render(request, 'core/partials/decks/new_varient.html', context)

def edit_flavor(request, flavor_pk):
    flavor = Flavor.objects.get(pk=flavor_pk)
    context = {}
    context['flavor'] = flavor
    context['form'] = FlavorForm(initial={
        'name':flavor.name,
        'deck': flavor.deck,
        'isdefault': flavor.isdefault,
    })
    return render(request, 'core/partials/decks/edit_flavor.html', context)

def edit_flavor_submit(request, flavor_pk):
    context = {}
    flavor = Flavor.objects.get(pk=flavor_pk)
    context['flavor'] = flavor
    if request.method == 'POST':
        form = FlavorForm(request.POST, instance=flavor)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'core/partials/decks/edit_flavor.html', context)
        
    return render(request, 'core/partials/decks/flavor_row.html', context)

def delete_flavor(request, flavor_pk):
    flavor = Flavor.objects.get(pk=flavor_pk)
    flavor.delete()
    return HttpResponse()