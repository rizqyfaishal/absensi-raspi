# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-19 03:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_auto_20180317_1840'),
    ]

    operations = [
        migrations.RenameField(
            model_name='absensi',
            old_name='NPM',
            new_name='Biodata',
        ),
    ]