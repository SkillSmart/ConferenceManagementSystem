# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-15 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SessionManagement', '0010_auto_20170314_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
