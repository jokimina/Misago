# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-15 09:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misago_users', '0015_user_agreements'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='wechat_openid',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
