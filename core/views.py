from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse 
from django import forms
from django.forms import modelform_factory
from .models import Deck, Flavor, MtgFormat, Archetype, League, Match
from users.models import User
from .forms import DeckForm, FlavorForm, LeagueForm, MatchForm
from django.db.models.functions import Lower
from django.db.models import Count, Q

def home(request):
    user = request.user
    try:
        current_league = League.objects.filter(user=request.user).latest('dateCreated')
        if current_league.isFinished:
            leaguecheck = 1
        else:
            leaguecheck = 0
    except:
        current_league = League.objects.none()
        leaguecheck = 1
    
    print(leaguecheck)

    context = {
        'leaguecheck': leaguecheck,

    }
    return render(request, "core/home.html", context)

def test(request):

    context = {

    }

    return render(request, "core/test.html", context)

#leagues
def add_league(request):


    decks = Deck.objects.all()
    context = {
        'decks': decks,
    }


    return render(request, 'core/partials/leaguematches/add_league.html', context)




def edit_match(request, match_pk):
    match = Match.objects.get(pk=match_pk)
    usernamelist = Match.objects.all().values("theirName").distinct().order_by(Lower("theirName"))
    print(usernamelist)
    decks = Deck.objects.all()
    context = {
        'match': match,
        'decks': decks,
        'usernamelist': usernamelist

    }

    return render(request, 'core/partials/leaguematches/edit_match.html', context)

def edit_match_submit(request, match_pk):
    context = {}
    match = Match.objects.get(pk=match_pk)
    context['match'] = match
    if request.method == 'POST':
        form = MatchForm()
        print("post here22", request.POST)
        match.theirName = request.POST.get('username')
        decknflavor = request.POST.get('decknflavor')
        if 'x' in decknflavor:
            xxy = decknflavor.split("x")
            print("yes x", xxy)
            match.theirDeck_id = xxy[0]
            match.theirFlavor_id = xxy[1]

        else:
            match.theirDeck_id = request.POST.get('decknflavor')
            match.theirFlavor = None
            print("no x")

        if 'game1ch' in request.POST:
            match.game1 = 1
            if 'game2ch' in request.POST:
                match.game2 = 1
                match.game3 = None
                match.didjawin = 1
            elif 'game3ch' in request.POST:
                match.game2 = 0
                match.game3 = 1
                match.didjawin = 1
            else:
                match.game2 = 0
                match.game3 = 0
                match.didjawin = 0 
        elif 'game2ch' in request.POST:
            match.game1 = 0 
            match.game2 = 1
            if 'game3ch' in request.POST:
                match.game3 = 1
                match.didjawin = 1
            else:
                match.game3 = 0
                match.didjawin = 0 
        else:
            match.game1 = 0
            match.game2 = 0 
            match.game3 = 0
            match.didjawin = 0


        match.save()
        league = League.objects.get(pk=match.league_id)
        total = 0
        for match in league.matches.all():
            if match.didjawin == True or match.didjawin == False:
                total += 1
            else:
                total += 0
        if total == 5:
            league.isFinished = True
            league.save()
                
    else:
        print("cancel button") 
        return render(request, 'core/partials/leaguematches/match_row.html', context)
    
    return render(request, 'core/partials/leaguematches/match_row.html', context)

def clear_match(request, match_pk):
    match = Match.objects.get(pk=match_pk)
    match.theirName = None
    match.theirDeck = None
    match.theirFlavor = None
    match.theirArchetype = None
    match.game1 = None
    match.game2 = None
    match.game3 = None
    match.didjawin = None
    match.save()
    context = {
        'match':match
    }
    print("match cleared: ", match)

    return render(request, 'core/partials/leaguematches/match_row.html', context)

def get_league_current(request):
    leagues_list = League.objects.all().order_by('-dateCreated')

    current_league = League.objects.latest('dateCreated')
    matches_list = current_league.matches.all()


    context = {
        "cLeague": current_league,
        "matches": matches_list
    }
    return render(request, 'core/partials/leaguematches/current_leaguetable.html', context)

def get_leagues_accordion(request):
    leagues_list = League.objects.filter(user=request.user, isFinished=True)
    leagues = leagues_list.annotate(wins=Count("matches", filter=Q(matches__didjawin=True))).order_by("-dateCreated")
    context = {
        "leagues": leagues
    }
    return render(request, 'core/partials/leaguematches/league_accordion.html', context)
def get_matches_table(request, league_pk):
    league = League.objects.get(pk=league_pk)
    matches_list = league.matches.all()
    context = {
        "matches": matches_list
    }
    return render(request, 'core/partials/leaguematches/matches_table.html', context)

def new_league_submit(request):
    user = request.user
    print("submit new league r")
    if request.method == 'POST':
        print(request.POST)
        decknflavor = request.POST.get('decknflavor')
        if 'x' in decknflavor:
            xxy = decknflavor.split("x")
            print("yes x", xxy)
            mydeckid = xxy[0]
            myflavorid = xxy[1]

        else:
            mydeckid = request.POST.get('decknflavor')
            myflavorid = 0
            print("no x")

        new_league = League.objects.create(
            user=user,
            mtgFormat_id=request.POST.get('mtgFormat'),
            myDeck_id=mydeckid,
            myFlavor_id=myflavorid
        )
        for i in range(1,6):
            Match.objects.create(
                league_id=new_league.pk,
                user=user,
                mtgFormat=new_league.mtgFormat,
                myDeck=new_league.myDeck,
                inLeagueNum=i,
                didjawin=None
            )


    context = {
    }

    return get_league_current(request)

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