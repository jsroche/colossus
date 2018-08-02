# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-07-05 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20180625_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sublibraryinformation',
            name='condition',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='experimental_condition'),
        ),
        migrations.AlterField(
            model_name='sublibraryinformation',
            name='pick_met',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='cell_call'),
        ),
    ]