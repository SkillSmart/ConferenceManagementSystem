# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-30 23:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SessionManagement', '0014_auto_20170331_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]