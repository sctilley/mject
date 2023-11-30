from django.contrib import admin

from .models import MtgFormat, Archetype, Deck, Flavor
from .models import League, Match


# Register your models here.
admin.site.register(MtgFormat)
admin.site.register(Archetype)
admin.site.register(Deck)
admin.site.register(Flavor)
admin.site.register(League)
admin.site.register(Match)