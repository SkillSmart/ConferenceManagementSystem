# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-03 16:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApplicationManagement', '0014_auto_20170403_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='q1_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='q2_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='q3_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='q4_score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
