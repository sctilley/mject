from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone



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