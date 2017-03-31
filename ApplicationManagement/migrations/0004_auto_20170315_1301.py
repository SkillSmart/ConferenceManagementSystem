# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-15 12:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApplicationManagement', '0003_auto_20170315_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='comment',
            field=models.TextField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='question_1',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='Question 1'),
        ),
        migrations.AlterField(
            model_name='review',
            name='question_2',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='Question 2'),
        ),
        migrations.AlterField(
            model_name='review',
            name='question_3',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='Question 3'),
        ),
        migrations.AlterField(
            model_name='review',
            name='question_4',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='Question 4'),
        ),
    ]