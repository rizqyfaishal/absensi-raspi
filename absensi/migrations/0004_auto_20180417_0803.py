# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-17 01:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('absensi', '0003_auto_20180417_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jadwal',
            name='hari',
            field=models.IntegerField(choices=[(0, 'Senin'), (1, 'Selasa'), (2, 'Rabu'), (3, 'Kamis'), (4, 'Jumat'), (5, 'Sabtu'), (7, 'Minggu')]),
        ),
    ]
