# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-17 10:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_auto_20180317_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='referensi',
            name='Password',
            field=models.CharField(default='', max_length=30),
        ),
    ]