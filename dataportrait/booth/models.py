from __future__ import unicode_literals
import os
import shutil
from django.db import models
from django.conf import settings

from PIL import Image
from portraitimage import portrait


class Photo(models.Model):
    code = models.CharField(max_length=4, unique=True)
    image = models.ImageField(upload_to='uploads/', blank=True)

    def image_tag(self):
        if self.image:
            return u'<img src="{0}{1}" width="150">'.format(settings.MEDIA_URL, self.image)
        else:
            return u''

    def save(self, *args, **kwargs):
        # if not self.id and not self.image:
        #     return

        super(Photo, self).save(*args, **kwargs)

        if not self.image:
            return

        img = Image.open(self.image)
        size = (900,900)
        crop_type = 'middle'

        # Get current and desired ratio for the images
        img_ratio = img.size[0] / float(img.size[1])
        ratio = size[0] / float(size[1])

        # The image is scaled/cropped vertically or horizontally depending on the ratio
        if ratio > img_ratio:
            img = img.resize((size[0], size[0] * img.size[1] // img.size[0]), Image.ANTIALIAS)
            # Crop in the top, middle or bottom
            if crop_type == 'top':
                box = (0, 0, img.size[0], size[1])
            elif crop_type == 'middle':
                box = (0, (img.size[1] - size[1]) // 2, img.size[0], (img.size[1] + size[1]) // 2)
            elif crop_type == 'bottom':
                box = (0, img.size[1] - size[1], img.size[0], img.size[1])
            else:
                raise ValueError('ERROR: invalid value for crop_type')
            img = img.crop(box)
        elif ratio < img_ratio:
            img = img.resize((size[1] * img.size[0] // img.size[1], size[1]), Image.ANTIALIAS)
            # Crop in the top, middle or bottom
            if crop_type == 'top':
                box = (0, 0, size[0], img.size[1])
            elif crop_type == 'middle':
                box = ((img.size[0] - size[0]) // 2, 0, (img.size[0] + size[0]) // 2, img.size[1])
            elif crop_type == 'bottom':
                box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
            else:
                raise ValueError('ERROR: invalid value for crop_type')
            img = img.crop(box)
        else:
            img = img.resize((size[0], size[1]), Image.ANTIALIAS)
            # If the scale is the same, we do not need to crop
        img.save(self.image.path)

        # create directory for storing code images
        target_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', self.code)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # copy image with code name to target directory
        image_name, image_ext = os.path.splitext(self.image.path)

        shutil.copyfile(self.image.path, target_dir + os.sep + self.code + '_base' + image_ext.lower())

        # call onUpload to save al layer
        portrait.onUpload(self.code, os.path.join(settings.MEDIA_ROOT, 'uploads'))


    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return self.code
