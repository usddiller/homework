from django.contrib import admin

from comments.models import Comments, LikeDislike


admin.site.register([Comments, LikeDislike])