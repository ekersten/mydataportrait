# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-23 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booth', '0005_merge_20160923_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='code',
            field=models.CharField(max_length=4, unique=True),
        ),
    ]
