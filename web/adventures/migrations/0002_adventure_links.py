# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-24 13:12
from __future__ import unicode_literals

import adventures.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adventures', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='adventure',
            name='links',
            field=adventures.models.URLListField(default=[]),
        ),
    ]
