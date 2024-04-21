from django.contrib import admin

from applications.common.admin import register_app_models
from applications.members.apps import MembersConfig
from applications.members.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {
            'fields':
                (
                    'username',
                    'password'
                )
        }),
        ('Personal info', {
            'fields': (
                'avatar',
                'first_name',
                'last_name',
                'email',
                'birth_date',
                'position',
                'time_preference',
                'about',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
    )



admin.site.register(User, UserAdmin)
register_app_models(app_name=MembersConfig.name)