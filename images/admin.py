from django.contrib import admin

from images.models import Image, Gallery


admin.site.register([Image, Gallery])
