# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-16 03:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('misago_core', '0003_delete_cacheversion'),
    ]

    operations = [
        migrations.CreateModel(
            name='CacheVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cache', models.CharField(max_length=128)),
                ('version', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
