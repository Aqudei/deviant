from django.contrib import admin
from .models import Deviation, Favor, User, DAUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class MyUserAdmin(UserAdmin):
    """
    docstring
    """
    list_display = UserAdmin.list_display + \
        ('da_username', 'da_userid', 'token')
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            "fields": (
                "da_username",
                "token",
                "da_userid"
            ),
        }),
    )


class DAUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'watchers_count',
                    'pageview_count', 'deviations_count', 'notes')
    search_fields = ('username', 'notes')
    # list_filter = ('watchers_count',)


@admin.register(Deviation)
class DeviationAdmin(admin.ModelAdmin):
    list_display = ('deviationid', 'title', 'owner')


@admin.register(Favor)
class FavorAdmin(admin.ModelAdmin):
    list_display = ('deviation', 'userid', 'thanked', 'owner')


admin.site.register(DAUser, DAUserAdmin)
admin.site.register(User, MyUserAdmin)
