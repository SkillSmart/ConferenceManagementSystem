# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-30 22:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SessionManagement', '0012_venue_booking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='venue',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='SessionManagement.Venue'),
            preserve_default=False,
        ),
    ]
