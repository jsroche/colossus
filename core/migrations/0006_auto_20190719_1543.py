# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-19 22:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190719_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='pipeline_tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.PipelineTag'),
        ),
    ]
