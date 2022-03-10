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
    token = models.JSONField(_("Token"), null=True, blank=True)
    da_userid = models.CharField(
        _("DA User Id"), max_length=100, null=True, blank=True)


class DAUser(models.Model):

    username = models.CharField(_("Username"), max_length=100)
    watchers_count = models.IntegerField(_("WatchersCount"), default=0)
    pageview_count = models.IntegerField(_("Page ViewCount"), default=0)
    deviations_count = models.IntegerField(_("DeviationsCount"), default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "User"), on_delete=models.CASCADE, null=True, blank=True)
    userid = models.UUIDField(_("DA User Id"), null=True, blank=True)
    notes = models.TextField(_("Notes"), null=True, blank=True)

    class Meta:
        verbose_name = _("Watcher")
        verbose_name_plural = _("Watchers")

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("dauser_detail", kwargs={"pk": self.pk})


class Deviation(models.Model):
    owner = models.ForeignKey("data.User", verbose_name=_(
        "Owner"), on_delete=models.SET_NULL, null=True)
    deviationid = models.UUIDField(_("Deviation Id"))
    title = models.CharField(_("Title"), max_length=250)

    class Meta:
        verbose_name = _("deviation")
        verbose_name_plural = _("deviations")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("deviation_detail", kwargs={"pk": self.pk})


class Favor(models.Model):
    deviation = models.ForeignKey(
        'data.Deviation', related_name='favors', on_delete=models.CASCADE)
    userid = models.UUIDField(_("Deviation Id"), null=True, blank=True)
    thanked = models.BooleanField(_("Thanked"), default=False)

    class Meta:
        verbose_name = _("Favor")
        verbose_name_plural = _("Favors")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Favor_detail", kwargs={"pk": self.pk})
