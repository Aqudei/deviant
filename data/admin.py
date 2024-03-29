from traceback import print_tb
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render

from data import forms
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import resolve
from django.db.models import Count

# Register your models here.


@admin.register(HookRequest)
class HookRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'headers', 'body']


@admin.register(User)
class MyUserAdmin(UserAdmin):
    """
    docstring
    """

    def re_authorize(self, obj):
        """
        docstring
        """
        return format_html("<a href='/init_auth'>Re-authorize App</a>")

    list_display = UserAdmin.list_display + \
        ('da_username', 'da_userid', 'token', 're_authorize')
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            "fields": (
                "da_username",
                "token",
                "da_userid",
                'patreon_token'
            ),
        }),
    )


@admin.action(description='Post to profile')
def post2profile(modeladmin, request, queryset):
    selected = queryset.values_list('pk', flat=True)
    return HttpResponseRedirect("/post2profile?ids={}".format(','.join(str(pk) for pk in selected)))


@admin.register(DAUser)
class DAUserAdmin(admin.ModelAdmin):
    @admin.display(description='Competitor Count', ordering='compete_count')
    def competitor_count(self, obj):
        """
        docstring
        """
        return obj.competitors.count()

    def get_queryset(self, request):
        """
        docstring
        """
        qs = super(DAUserAdmin, self).get_queryset(request)
        return qs.annotate(compete_count=Count('competitors'))

    list_display = ('username', 'watchers_count', 'pageview_count',
                    'deviations_count', 'competitor_count', 'notes', 'updated_at', 'created_at')
    search_fields = ('username', 'notes')
    # list_filter = ('watchers_count',)
    actions = [post2profile]


@admin.register(Deviation)
class DeviationAdmin(admin.ModelAdmin):
    list_display = ('deviationid', 'title', 'owner', 'favourites')


@admin.register(Favor)
class FavorAdmin(admin.ModelAdmin):
    list_display = ('deviation', 'userid', 'owner', 'fav_timestamp')


@admin.action(description='Mark selected as Sent')
def mark_sent(modeladmin, request, queryset):
    queryset.update(sent=True)


@admin.register(Thank)
class ThankAdmin(admin.ModelAdmin):
    list_display = ('owner', 'userid', 'username',
                    'sent', 'sent_timestamp', 'message', 'created_at', 'updated_at')
    list_filter = ('sent',)
    actions = [mark_sent]


@admin.register(Competitor)
class CompetitorAdmin(admin.ModelAdmin):
    list_display = ('owner', 'da_username', 'da_userid', 'perc_shared_watchers', 'total_submission',
                    'total_watchers', 'total_pageviews', 'date_started', 'created_at', 'updated_at')


@admin.register(MyTask)
class MyTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'last_ran', 'last_error')

    def last_error(self, obj):
        """
        docstring
        """
        if obj.last_error:
            return obj.last_error[:20]

        return obj.last_error
