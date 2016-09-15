from __future__ import unicode_literals
from django.db import models
from django.conf import settings


class Photo(models.Model):
    code = models.CharField(max_length=30)
    image = models.ImageField(upload_to='uploads/')

    def image_tag(self):
        return u'<img src="{0}{1}" width="150">'.format(settings.MEDIA_URL, self.image)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Photo, self).delete(*args, **kwargs)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
