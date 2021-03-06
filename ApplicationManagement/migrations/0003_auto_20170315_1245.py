# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-15 11:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApplicationManagement', '0002_auto_20170315_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='question_1',
            field=models.CharField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1, max_length=1, verbose_name='Question 1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='question_2',
            field=models.CharField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1, max_length=1, verbose_name='Question 2'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='question_3',
            field=models.CharField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1, max_length=1, verbose_name='Question 3'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='question_4',
            field=models.CharField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1, max_length=1, verbose_name='Question 4'),
            preserve_default=False,
        ),
    ]
