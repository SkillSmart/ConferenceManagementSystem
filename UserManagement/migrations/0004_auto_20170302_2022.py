# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-02 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0003_auto_20170302_2009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expertprofile',
            name='expertRole',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='studentRole',
        ),
        migrations.AddField(
            model_name='attendent',
            name='role',
            field=models.CharField(choices=[('negotiator', 'Negotiator'), ('mediator', 'Mediator'), ('expert', 'Expert Assessor'), ('coach', 'Coach'), ('assessor', 'Assessor')], default='', max_length=35),
            preserve_default=False,
        ),
    ]
