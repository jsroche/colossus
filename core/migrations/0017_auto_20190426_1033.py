# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-04-26 17:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pbal', '0004_auto_20190426_1033'),
        ('core', '0016_rename_table_tenx'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaltenxchip',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltenxlane',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltenxlane',
            name='sequencing',
        ),
        migrations.RemoveField(
            model_name='historicaltenxlibrary',
            name='chips',
        ),
        migrations.RemoveField(
            model_name='historicaltenxlibrary',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltenxlibrary',
            name='sample',
        ),
        migrations.RemoveField(
            model_name='historicaltenxlibraryconstructioninformation',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltenxlibraryconstructioninformation',
            name='library',
        ),
        migrations.RemoveField(
            model_name='historicaltenxlibraryquantificationandstorage',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltenxlibraryquantificationandstorage',
            name='library',
        ),
        migrations.RemoveField(
            model_name='historicaltenxlibrarysampledetail',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltenxlibrarysampledetail',
            name='library',
        ),
        migrations.RemoveField(
            model_name='historicaltenxsequencing',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltenxsequencing',
            name='library',
        ),
        migrations.RemoveField(
            model_name='historicaltenxsequencing',
            name='tenx_pool',
        ),
        migrations.RemoveField(
            model_name='tenxlane',
            name='sequencing',
        ),
        migrations.RemoveField(
            model_name='tenxlibrary',
            name='chips',
        ),
        migrations.RemoveField(
            model_name='tenxlibrary',
            name='projects',
        ),
        migrations.RemoveField(
            model_name='tenxlibrary',
            name='relates_to_dlp',
        ),
        migrations.RemoveField(
            model_name='tenxlibrary',
            name='relates_to_tenx',
        ),
        migrations.RemoveField(
            model_name='tenxlibrary',
            name='sample',
        ),
        migrations.RemoveField(
            model_name='tenxlibraryconstructioninformation',
            name='library',
        ),
        migrations.RemoveField(
            model_name='tenxlibraryquantificationandstorage',
            name='library',
        ),
        migrations.RemoveField(
            model_name='tenxlibrarysampledetail',
            name='library',
        ),
        migrations.RemoveField(
            model_name='tenxpool',
            name='libraries',
        ),
        migrations.AlterUniqueTogether(
            name='tenxsequencing',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='tenxsequencing',
            name='analysis',
        ),
        migrations.RemoveField(
            model_name='tenxsequencing',
            name='library',
        ),
        migrations.RemoveField(
            model_name='tenxsequencing',
            name='tenx_pool',
        ),
        migrations.AlterField(
            model_name='analysis',
            name='tenx_lanes',
            field=models.ManyToManyField(blank=True, to='tenx.TenxLane'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='tenx_library',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tenx.TenxLibrary'),
        ),
        migrations.AlterField(
            model_name='dlplibrary',
            name='relates_to_tenx',
            field=models.ManyToManyField(blank=True, to='tenx.TenxLibrary', verbose_name='Relates to (Tenx)'),
        ),
        migrations.DeleteModel(
            name='HistoricalTenxChip',
        ),
        migrations.DeleteModel(
            name='HistoricalTenxLane',
        ),
        migrations.DeleteModel(
            name='HistoricalTenxLibrary',
        ),
        migrations.DeleteModel(
            name='HistoricalTenxLibraryConstructionInformation',
        ),
        migrations.DeleteModel(
            name='HistoricalTenxLibraryQuantificationAndStorage',
        ),
        migrations.DeleteModel(
            name='HistoricalTenxLibrarySampleDetail',
        ),
        migrations.DeleteModel(
            name='HistoricalTenxSequencing',
        ),
        migrations.DeleteModel(
            name='TenxChip',
        ),
        migrations.DeleteModel(
            name='TenxLane',
        ),
        migrations.DeleteModel(
            name='TenxLibrary',
        ),
        migrations.DeleteModel(
            name='TenxLibraryConstructionInformation',
        ),
        migrations.DeleteModel(
            name='TenxLibraryQuantificationAndStorage',
        ),
        migrations.DeleteModel(
            name='TenxLibrarySampleDetail',
        ),
        migrations.DeleteModel(
            name='TenxPool',
        ),
        migrations.DeleteModel(
            name='TenxSequencing',
        ),
    ]
