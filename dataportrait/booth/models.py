from __future__ import unicode_literals
from django.db import models
from django.conf import settings


class Photo(models.Model):
    code = models.CharField(max_length=4)
    image = models.ImageField(upload_to='uploads/', blank=True)

    def image_tag(self):
        if self.image:
            return u'<img src="{0}{1}" width="150">'.format(settings.MEDIA_URL, self.image)
        else:
            return u''

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Photo, self).delete(*args, **kwargs)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
