from django import forms
from .models import Archetype, Deck, Flavor, League, Match


class DeckForm(forms.ModelForm):
    flavorname = forms.CharField(label="flavor name", max_length=225, required=False)
    fisdefault = forms.BooleanField(label='Make Default Varient', required=False, widget=forms.CheckboxInput(attrs={'class': 'largerCheckbox'}))

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
    forms.ModelChoiceField(queryset=Flavor.objects.all(), label='Variant', widget=forms.Select(attrs={'disabled': 'disabled'}))
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
    class Meta:
        model = League
        fields = (
            'mtgFormat',
            'myDeck',
            'myFlavor'
        )
