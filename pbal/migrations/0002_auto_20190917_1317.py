# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-09-17 20:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pbal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpballibraryquantificationandstorage',
            name='qc_check',
            field=models.CharField(blank=True, choices=[('P', 'Will sequence'), ('N', 'Will not sequence'), ('H', 'On Hold')], max_length=50, null=True, verbose_name='QC check'),
        ),
        migrations.AlterField(
            model_name='pballibraryquantificationandstorage',
            name='qc_check',
            field=models.CharField(blank=True, choices=[('P', 'Will sequence'), ('N', 'Will not sequence'), ('H', 'On Hold')], max_length=50, null=True, verbose_name='QC check'),
        ),
    ]
