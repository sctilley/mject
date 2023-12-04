from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recentFormat = models.ForeignKey('core.MtgFormat', null=True, on_delete=models.CASCADE)
    recentDeck = models.ForeignKey('core.Deck', null=True, on_delete=models.CASCADE)
    recentFlavor = models.ForeignKey('core.Flavor', null=True, on_delete=models.CASCADE)
    mtgoUserName = models.CharField(null=True, max_length=80)

    def __str__(self):
        return f'{self.user} Profile'