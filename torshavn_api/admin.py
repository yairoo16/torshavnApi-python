from django.contrib import admin
from torshavn_api import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.ProfileFeedItem)
admin.site.register(models.Marker)
