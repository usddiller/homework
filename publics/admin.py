from django.contrib import admin

from publics.models import Public, PublicInvite


admin.site.register([Public, PublicInvite])
