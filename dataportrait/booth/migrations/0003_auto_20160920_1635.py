# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-20 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booth', '0002_auto_20160916_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='code',
            field=models.CharField(max_length=4, unique=True),
        ),
    ]
