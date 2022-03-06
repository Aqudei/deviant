from django.contrib import admin
from .models import User, DAUser
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
            ),
        }),
    )


class DAUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'watchers_count',
                    'pageview_count', 'deviations_count')
    search_fields = ('username',)
    # list_filter = ('watchers_count',)


admin.site.register(DAUser, DAUserAdmin)


admin.site.register(User, MyUserAdmin)
