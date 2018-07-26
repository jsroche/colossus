# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-08-03 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sisyphus', '0010_auto_20180625_1651'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dlpanalysisinformation',
            name='tantalus_path',
        ),
        migrations.RemoveField(
            model_name='pbalanalysisinformation',
            name='tantalus_path',
        ),
        migrations.RemoveField(
            model_name='tenxanalysisinformation',
            name='tantalus_path',
        ),
        migrations.AddField(
            model_name='dlpanalysisinformation',
            name='blob_path',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Blob path'),
        ),
        migrations.AddField(
            model_name='pbalanalysisinformation',
            name='blob_path',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Blob path'),
        ),
        migrations.AddField(
            model_name='tenxanalysisinformation',
            name='blob_path',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Blob path'),
        ),
    ]
