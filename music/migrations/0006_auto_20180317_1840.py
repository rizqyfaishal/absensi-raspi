# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-17 11:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_auto_20180317_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='absensi',
            name='Email_Sended',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='absensi',
            name='Random_Text',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]