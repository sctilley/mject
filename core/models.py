from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from users.models import CustomUser



class MtgFormat(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Archetype(models.Model):
    name = models.CharField(verbose_name="Archetype", max_length=40)
    mtgFormat = models.ForeignKey(MtgFormat, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class Deck(models.Model):
    name = models.CharField(verbose_name="deck name", max_length=25)
    mtgFormat = models.ForeignKey(MtgFormat, null=True, on_delete=models.CASCADE)
    archetype = models.ForeignKey(Archetype, null=True, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)

class Flavor(models.Model):

    name = models.CharField(max_length=30, default='none')
    deck = models.ForeignKey(Deck, null=True, on_delete=models.CASCADE, related_name="flavors")
    isdefault = models.BooleanField('default', default=False)

    def __str__(self):
        return f'{self.name}'

# leagues and matches

class League(models.Model):
    mtgFormat = models.ForeignKey(MtgFormat, null=True, on_delete=models.CASCADE, related_name="mformat")
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(default=timezone.now)
    myDeck = models.ForeignKey(Deck, null=True, on_delete=models.CASCADE, related_name="mydeckl")
    myFlavor = models.ForeignKey(Flavor, null=True, default=None, on_delete=models.CASCADE, related_name="myflavorl")
    isFinished = models.BooleanField('finished', default=False)

    def __str__(self):
        return f'{self.mtgFormat} League with {self.myDeck} by {self.user} on {self.dateCreated}'

    def get_absolute_url(self):
        return reverse('leaguedetail', kwargs={'pk': self.pk})



class Match(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(default=timezone.now, null=True)
    mtgFormat = models.ForeignKey(MtgFormat, null=True, on_delete=models.CASCADE, related_name="mtgFormat")
    myDeck = models.ForeignKey(Deck, null=True, on_delete=models.CASCADE, related_name="mydeck")

    theirName = models.CharField(null=True, max_length=100)
    theirArchetype = models.ForeignKey(Archetype, verbose_name="Their Archetype", null=True, on_delete=models.CASCADE, related_name="theirarchetype")
    theirDeck = models.ForeignKey(Deck, verbose_name="Their Deck", null=True, on_delete=models.CASCADE, related_name="theirdeck")
    theirFlavor = models.ForeignKey(Flavor, verbose_name="Thier Flavor", null=True, on_delete=models.CASCADE, related_name="theirflavors")

    inLeagueNum = models.IntegerField(null=True)
    game1 = models.BooleanField(verbose_name='Win1', null=True, default=None, help_text="win")
    game2 = models.BooleanField(verbose_name='Win2', null=True, default=None)
    game3 = models.BooleanField(verbose_name='Win3', null=True, default=None)
    didjawin = models.BooleanField('Match Win', null=True, default=None)

    league = models.ForeignKey(League, null=True, on_delete=models.CASCADE, related_name="matches")

    def __str__(self):
        return f'Match vs: {self.theirName} by {self.user} on {self.dateCreated} (league id {self.league.pk})'