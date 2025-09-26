from django.contrib import admin

from users.models import Client, FriendInvite


admin.site.register(Client)
admin.site.register(FriendInvite)
