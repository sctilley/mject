from django import forms
from .models import MtgFormat, Archetype, Deck, Flavor, League, Match


class DeckForm(forms.ModelForm):
    flavorname = forms.CharField(label="flavor name", max_length=225, required=False)
    fisdefault = forms.BooleanField(label='Make Default Varient', required=False, widget=forms.CheckboxInput(attrs={'class': 'largerCheckbox'}))
    mtgFormat = forms.ModelChoiceField(queryset=MtgFormat.objects.all(), initial=0)


    class Meta:
        model = Deck
        fields = (
            'name',
            'flavorname',
            'fisdefault',
            'mtgFormat',
            'archetype'
        )


class FlavorForm(forms.ModelForm):
    name = forms.CharField(label="varient name")
    isdefault = forms.BooleanField(label='Make Default Varient', required=False, widget=forms.CheckboxInput(attrs={'class': 'largerCheckbox'}))

    class Meta:
        model = Flavor
        fields = (
            'deck',
            'name',
            'isdefault',
        )

class LeagueForm(forms.ModelForm):
    mtgFormat = forms.ModelChoiceField(queryset=MtgFormat.objects.all(), initial=0)
    
    class Meta:
        model = League
        fields = (
            'mtgFormat',
            'myFlavor'
        )

class MatchForm(forms.ModelForm):
    theirName = forms.CharField(required=True, max_length=100, label='Their Name')
    theirDeck = forms.ModelChoiceField(required=False, queryset=Deck.objects.filter(mtgFormat=1).order_by('name'), label='Their Deck')
    theirFlavor = forms.ModelChoiceField(required=False, queryset=Flavor.objects.all().order_by('name'), label='Their Flavor')
    
    game1 = forms.BooleanField(label='one', required=False, widget=forms.CheckboxInput(
        attrs={'class': 'largerCheckbox', 'title': 'This is game 1. Tick the box if you won.'}))
    game2 = forms.BooleanField(label='two', required=False, widget=forms.CheckboxInput(
        attrs={'class': 'largerCheckbox', 'title': 'This is game 2. Tick the box if you won.'}))
    game3 = forms.BooleanField(label='three', required=False, widget=forms.CheckboxInput(
        attrs={'class': 'largerCheckbox', 'title': 'This is game 3. Tick the box if you won.'}))

    class Meta:
        model = Match
        fields = (
            'theirName',
            'theirFlavor',
            'game1',
            'game2',
            'game3',
        )