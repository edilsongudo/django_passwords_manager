from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'is_staff', 'is_superuser')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('email',)
    search_fields = ('first_name', 'last_name', 'email')  # 🖘 no username
    fieldsets = (
        (
            'Fields',
            {
                'fields': (
                    'email',
                    'date_joined',
                    'last_login',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                    'password',
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
                #              🖞 without username
            },
        ),
    )


# admin.site.register(User, CustomUserAdmin)
