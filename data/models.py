from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    da_username = models.CharField(
        _("Deviant Username"), max_length=100, null=True, blank=True, unique=True)


class DAUser(models.Model):

    username = models.CharField(_("Username"), max_length=100)
    watchers_count = models.IntegerField(_("WatchersCount"), default=0)
    pageview_count = models.IntegerField(_("Page ViewCount"), default=0)
    deviations_count = models.IntegerField(_("DeviationsCount"), default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "User"), on_delete=models.CASCADE, null=True, blank=True)
    userid = models.UUIDField(_("DA User Id"), null=True, blank=True)

    class Meta:
        verbose_name = _("dauser")
        verbose_name_plural = _("dausers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("dauser_detail", kwargs={"pk": self.pk})
