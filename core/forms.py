from django import forms
from .models import Archetype, Deck, Flavor


class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = (
            'name',
            'mtgFormat',
            'archetype'
        )

class FlavorForm(forms.ModelForm):
    forms.ModelChoiceField(queryset=Flavor.objects.all(), label='Variant', widget=forms.Select(attrs={'disabled': 'disabled'}))
    name = forms.CharField(
        label="varient name", widget=forms.TextInput(attrs={'class': 'redtest2'}))
    isdefault = forms.BooleanField(label='Make Default Varient', required=False, widget=forms.CheckboxInput(
        attrs={'class': 'largerCheckbox'}))

    class Meta:
        model = Flavor
        fields = (
            'deck',
            'name',
            'isdefault',
        )