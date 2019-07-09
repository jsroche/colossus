# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-02 2329
from __future__ import unicode_literals

from django.db import migrations

keymap = {
    87 :"SC-2392",
    141 :"SC-2393",
    142 :"SC-2394",
    143 :"SC-2395",
    144 :"SC-2396",
    145 :"SC-2397",
    146 :"SC-2398",
    147 :"SC-2399",
    148 :"SC-2400",
    149 :"SC-2401",
    150 :"SC-2402",
    151: "SC-2403",
    152 :"SC-2404",
    153 :"SC-2405",
    154 :"SC-2406",
    155 :"SC-2407",
    156 :"SC-2408",
    157 :"SC-2409",
    158 :"SC-2410",
    159 :"SC-2411",
    160 :"SC-2412",
    161 :"SC-2413",
    162 :"SC-2414",
    163 :"SC-2415",
    164 :"SC-2416",
    165 :"SC-2417",
    166 :"SC-2418",
    167 :"SC-2419",
    168 :"SC-2420",
    169 :"SC-2421",
    170 :"SC-2422",
    171 :"SC-2423",
    172 :"SC-2424",
    173 :"SC-2425",
    174 :"SC-2426",
    175 :"SC-2427",
    176 :"SC-2428",
    177 :"SC-2429",
    178 :"SC-2430",
    179 :"SC-2431",
    182 :"SC-2432",
    183 :"SC-2433",
    184 :"SC-2434",
    185 :"SC-2435",
    186 :"SC-2436",
    187 :"SC-2437",
    188 :"SC-2438",
    189 :"SC-2439",
    190 :"SC-2440",
    191 :"SC-2441",
    192 :"SC-2442",
    193 :"SC-2443",
    194 :"SC-2444",
    195 :"SC-2445",
    196 :"SC-2446",
    197 :"SC-2447",
    198 :"SC-2448",
    199 :"SC-2449",
    200 :"SC-2450",
    201 :"SC-2451",
    202 :"SC-2452",
    203 :"SC-2453",
    204 :"SC-2454",
    205 :"SC-2455",
    231 :"SC-2456"
    }

def tenx_jira_update(apps, schema_editor):
    tenx_library = apps.get_model('tenx', 'TenxLibrary')
    for library in tenx_library.objects.filter(id__in=keymap.keys()):
        library.jira_ticket = keymap[library.id]
        library.save()


class Migration(migrations.Migration):

    dependencies = [
        ('tenx', '0006_auto_20190516_1259'),
    ]

    operations = [
        migrations.RunPython(tenx_jira_update)
    ]