# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-15 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0024_auto_20170315_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendent',
            name='uni_team',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
