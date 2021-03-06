# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApplicationManagement', '0023_auto_20170405_2058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='status',
        ),
        migrations.AddField(
            model_name='application',
            name='review_status',
            field=models.IntegerField(choices=[(1, 'Unreviewed'), (2, 'Reviewed'), (3, 'Selected')], default=1),
        ),
        migrations.AddField(
            model_name='application',
            name='selection_status',
            field=models.IntegerField(choices=[(1, 'None'), (2, 'Declined'), (3, 'Accepted')], default=1),
        ),
    ]
