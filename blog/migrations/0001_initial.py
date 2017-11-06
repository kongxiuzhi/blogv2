# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-31 12:57
from __future__ import unicode_literals

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('content', ckeditor.fields.RichTextField(verbose_name='内容')),
                ('view', models.IntegerField(default=0, verbose_name='浏览量')),
                ('click', models.IntegerField(default=0, verbose_name='点赞')),
                ('publish', models.BooleanField(default=True, verbose_name='是否发表')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'ordering': ('created',),
            },
            managers=[
                ('getPublished', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor.fields.RichTextField(verbose_name='内容')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('active', models.BooleanField(default=True, verbose_name='激活')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.Article')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=11, verbose_name='电话')),
                ('sex', models.CharField(choices=[('男', '男'), ('女', '女'), ('保密', '保密')], default='男', max_length=2, verbose_name='性别')),
                ('avatar', models.ImageField(default='avatar/defa/avatar.jpg', max_length=200, upload_to='avatar/%Y/%m/%d', verbose_name='头像')),
                ('level', models.CharField(choices=[('1', '虾米'), ('2', '小鱼'), ('3', '大鱼'), ('4', '鲨鱼'), ('5', '虎鲸'), ('6', '渔夫'), ('0', '污泥')], default='1', max_length=2, verbose_name='级别')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
