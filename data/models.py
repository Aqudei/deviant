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


class Thank(models.Model):

    owner = models.ForeignKey(User, verbose_name=_(
        "Owner"), on_delete=models.CASCADE)
    userid = models.UUIDField(_("DA User Id"))
    username = models.CharField(
        _("Username"), max_length=255, null=True, blank=True)
    sent = models.BooleanField(_("Sent"), default=False)
    sent_timestamp = models.DateTimeField(
        _("Sent Timestamp"), auto_now=False, auto_now_add=False, null=True, blank=True)
    message = models.TextField(_("Message"), default='Thanks for the fav!')
    updated_at = models.DateTimeField(
        _("Updated At"), auto_now=True, auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(
        _("Created At"), auto_now=False, auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = _("thank")
        verbose_name_plural = _("thanks")
        unique_together = [['owner', 'userid']]

    def __str__(self):
        return f"{self.userid}"

    def get_absolute_url(self):
        return reverse("thank_detail", kwargs={"pk": self.pk})


class DAUser(models.Model):

    username = models.CharField(_("Username"), max_length=100)
    watchers_count = models.IntegerField(_("WatchersCount"), default=0)
    pageview_count = models.IntegerField(_("Page ViewCount"), default=0)
    deviations_count = models.IntegerField(_("DeviationsCount"), default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "User"), on_delete=models.CASCADE, null=True, blank=True)
    userid = models.UUIDField(_("DA User Id"), null=True, blank=True)
    notes = models.TextField(_("Notes"), null=True, blank=True)

    updated_at = models.DateTimeField(
        _("Updated At"), auto_now=True, auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(
        _("Created At"), auto_now=False, auto_now_add=True, null=True, blank=True)

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
    favourites = models.IntegerField(_("Favourites"))

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
    userid = models.UUIDField(_("User Id"), null=True, blank=True)
    owner = models.ForeignKey("data.User", verbose_name=_(
        "Owner"), on_delete=models.SET_NULL, null=True)
    username = models.CharField(
        _("Username"), max_length=150, null=True, blank=True)
    fav_timestamp = models.IntegerField(_("Fav Timestamp"), default=0)

    class Meta:
        verbose_name = _("Favor")
        verbose_name_plural = _("Favors")

    def __str__(self):
        return f"{self.userid}-{self.owner}"

    def get_absolute_url(self):
        return reverse("Favor_detail", kwargs={"pk": self.pk})


class Competitor(models.Model):

    owner = models.ForeignKey(User, verbose_name=_(
        "Owner"), on_delete=models.CASCADE)
    da_username = models.CharField(
        _("Deviant Username"), max_length=100, unique=True)
    da_userid = models.CharField(
        _("DA User Id"), max_length=100, null=True, blank=True)
    perc_shared_watchers = models.FloatField(
        _("Percent Shared Watchers"), default=0.0)
    total_submission = models.IntegerField(_("Total Submissions"), default=0)
    total_watchers = models.IntegerField(_("Total Watchers"), default=0)
    total_pageviews = models.IntegerField(_("Total Pageviews"), default=0)
    date_started = models.DateTimeField(
        _("Date Started"), auto_now=False, auto_now_add=False, null=True, blank=True)

    updated_at = models.DateTimeField(
        _("Updated At"), auto_now=True, auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(
        _("Created At"), auto_now=False, auto_now_add=True, null=True, blank=True)

    watchers = models.ManyToManyField(
        "data.DAUser", verbose_name=_("Watchers"), related_name='competitors', blank=True)

    class Meta:
        verbose_name = _("competitor")
        verbose_name_plural = _("competitors")

    def __str__(self):
        return self.da_username

    def get_absolute_url(self):
        return reverse("competitor_detail", kwargs={"pk": self.pk})


class MyTask(models.Model):
    STATUSES = (('RUNNING', 'RUNNING'), ('IDLE', 'IDLE'))
    NAMES = (('COMPETITORS', 'COMPETITORS'), ('FAVOURITES', 'FAVOURITES'),
             ('DEVIATIONS', 'DEVIATIONS'), ('COMPETITOR_WATCHERS', 'COMPETITOR_WATCHERS'))

    owner = models.ForeignKey("data.User", verbose_name=_(
        "User"), on_delete=models.CASCADE)
    name = models.CharField(_("Task"), max_length=50, choices=NAMES)
    status = models.CharField(
        _("Status"), max_length=50, choices=STATUSES, default='IDLE')
    last_ran = models.DateTimeField(
        _("Last Ran"), auto_now=True, auto_now_add=False, null=True, blank=True)
    last_error = models.TextField(_("Last Error"), blank=True, null=True)

    class Meta:
        verbose_name = _("My Task")
        verbose_name_plural = _("My Tasks")
        unique_together = ['owner', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("mytask_detail", kwargs={"pk": self.pk})
