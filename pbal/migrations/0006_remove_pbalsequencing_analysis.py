# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-11 23:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbal', '0005_auto_20190509_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pbalsequencing',
            name='analysis',
        ),
    ]
