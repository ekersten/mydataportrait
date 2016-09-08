from django.contrib import admin

from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('code', 'image_tag')
    exclude = ('image_tag',)

admin.site.register(Photo, PhotoAdmin)