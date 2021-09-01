from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from model_utils.models import TimeStampedModel

User = get_user_model()


class UserProfile(TimeStampedModel):
    """Профиль пользователя."""
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    city = models.ForeignKey("main.City", on_delete=models.PROTECT, default=None, null=True, blank=True)

    class Meta:
        verbose_name = _("User profile")
        verbose_name_plural = _("User profiles")


class City(TimeStampedModel):
    """Город."""
    name = models.CharField(_("name"), max_length=200)

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")


class Advert(TimeStampedModel):
    """Объявление"""
    name = models.CharField(_("name"), max_length=200)
    city = models.ForeignKey("main.City", on_delete=models.PROTECT, default=None, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, null=True, blank=True)
    body = models.TextField(_("body"), blank=True)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = _("Advert")
        verbose_name_plural = _("Adverts")
