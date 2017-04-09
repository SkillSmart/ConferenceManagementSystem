# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-08 15:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0035_auto_20170408_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('attendent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='UserManagement.Attendent')),
            ],
            bases=('UserManagement.attendent',),
        ),
        migrations.CreateModel(
            name='StaffProfile',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='UserManagement.Profile')),
                ('staff', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='UserManagement.Staff')),
            ],
            bases=('UserManagement.profile',),
        ),
    ]