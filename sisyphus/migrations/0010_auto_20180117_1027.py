# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-01-17 18:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20180115_1449'),
        ('sisyphus', '0009_auto_20180116_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='pbalanalysisinformation',
            name='library',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.DlpLibrary', verbose_name='Library'),
        ),
        migrations.AddField(
            model_name='tenxanalysisinformation',
            name='library',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.DlpLibrary', verbose_name='Library'),
        ),
    ]
