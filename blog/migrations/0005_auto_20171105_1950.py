# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-05 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20171105_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='电话'),
        ),
    ]
