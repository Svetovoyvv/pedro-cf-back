from django.contrib import admin

from applications.chats.apps import ChatsConfig
from applications.chats.models import Chat
from applications.common.admin import register_app_models


class ChatAdmin(admin.ModelAdmin):
    readonly_fields = ('pk', )


admin.site.register(Chat, ChatAdmin)
register_app_models(app_name=ChatsConfig.name)
