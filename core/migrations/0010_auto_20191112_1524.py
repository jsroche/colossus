# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-11-12 23:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20190724_1210'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicaladditionalsampleinformation',
            old_name='additional_pathology_info',
            new_name='receptor_status',
        ),
        migrations.RenameField(
            model_name='additionalsampleinformation',
            old_name='additional_pathology_info',
            new_name='receptor_status',
        ),
        migrations.RenameField(
            model_name='historicaladditionalsampleinformation',
            old_name='treatment_status',
            new_name='sample_treatment_status',
        ),
        migrations.RenameField(
            model_name='additionalsampleinformation',
            old_name='treatment_status',
            new_name='sample_treatment_status',
        ),
        migrations.AddField(
            model_name='historicaladditionalsampleinformation',
            name='patient_treatment_status',
            field=models.CharField(
                blank=True,
                choices=[
                    ('PR', 'Pre-treatment'),
                    ('IN', 'In-treatment'),
                    ('PO', 'Post-treatment'),
                    ('NA', 'N/A'),
                    ('UN', 'Unknown'),
                ],
                max_length=50,
                null=True,
                verbose_name='Patient treatment status',
            ),
        ),
        migrations.AddField(
            model_name='additionalsampleinformation',
            name='patient_treatment_status',
            field=models.CharField(
                blank=True,
                choices=[
                    ('PR', 'Pre-treatment'),
                    ('IN', 'In-treatment'),
                    ('PO', 'Post-treatment'),
                    ('NA', 'N/A'),
                    ('UN', 'Unknown'),
                ],
                max_length=50,
                null=True,
                verbose_name='Patient treatment status',
            ),
        ),
    ]