from django.contrib import admin

from chats.models import Chat, Message


admin.site.register([Chat, Message])
