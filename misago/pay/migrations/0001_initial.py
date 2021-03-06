# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-11 10:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('deleted', models.BooleanField(default=False, verbose_name='是否已删除')),
                ('body', models.CharField(max_length=256, verbose_name='商品描述')),
                ('out_trade_no', models.CharField(max_length=64, unique=True, verbose_name='订单号')),
                ('transaction_id', models.CharField(default='', max_length=64, verbose_name='微信支付订单号')),
                ('total_fee', models.BigIntegerField(verbose_name='订单的资金总额,单位为分')),
                ('product_id', models.CharField(max_length=16, verbose_name='商品ID')),
                ('notify_url', models.CharField(max_length=500, verbose_name='支付完成通知url')),
                ('pay_time', models.DateTimeField(blank=True, null=True, verbose_name='支付时间')),
                ('status', models.CharField(choices=[('NOT_PAY', '未支付'), ('SUCCESS', '支付成功'), ('CLOSED', '已关闭'), ('PAY_ERROR', '支付错误'), ('REFUND', '已退款')], max_length=16, verbose_name='订单状态')),
                ('trade_type', models.CharField(choices=[('NOT_PAY', '未支付'), ('SUCCESS', '支付成功'), ('CLOSED', '已关闭'), ('PAY_ERROR', '支付错误'), ('REFUND', '已退款')], max_length=16, verbose_name='订单状态')),
                ('appid', models.CharField(blank=True, max_length=32, null=True)),
                ('mchid', models.CharField(blank=True, max_length=16, null=True)),
                ('prepay_id', models.CharField(blank=True, max_length=64, null=True, unique=True, verbose_name='支付唯一订单号')),
                ('code_url', models.CharField(blank=True, max_length=100, null=True, verbose_name='二维码地址')),
                ('nonce_str', models.CharField(blank=True, max_length=32, null=True, verbose_name='随机字符串')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '微信订单',
                'verbose_name_plural': '微信订单',
                'ordering': ('-created_time',),
            },
        ),
    ]
