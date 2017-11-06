# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-05 03:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_auto_20171104_0757'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='folower',
            field=models.ManyToManyField(blank=True, related_name='likearticles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
    ]
