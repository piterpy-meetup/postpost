from django.contrib import admin

from api import models


class PublicationAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(models.Publication, PublicationAdmin)
admin.site.register(models.PlatformPost)