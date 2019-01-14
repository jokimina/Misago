from django.db import models
from misago.core.models import BaseModel
from misago.users.models.user import User


class Order(BaseModel):
    NOT_PAY = 'NOT_PAY'
    SUCCESS = 'SUCCESS'
    CLOSED = 'CLOSED'
    PAY_ERROR = 'PAY_ERROR'
    REFUND = 'REFUND'

    STATUS_CHOICES = (
        (NOT_PAY, "未支付"),
        (SUCCESS, "支付成功"),
        (CLOSED, "已关闭"),
        (PAY_ERROR, "支付错误"),
        (REFUND, "已退款"),
    )

    user = models.ForeignKey(User)
    body = models.CharField(max_length=256, verbose_name='商品描述')
    out_trade_no = models.CharField(max_length=64, unique=True, verbose_name='订单号')
    transaction_id = models.CharField(default='', max_length=64, verbose_name='微信支付订单号')
    total_fee = models.BigIntegerField(verbose_name='订单的资金总额,单位为分')
    product_id = models.CharField(max_length=16, verbose_name='商品ID')
    notify_url = models.CharField(max_length=500, verbose_name='支付完成通知url')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    status = models.CharField(max_length=16, verbose_name="订单状态", choices=STATUS_CHOICES)
    trade_type = models.CharField(max_length=16, verbose_name="订单状态", choices=STATUS_CHOICES)
    appid = models.CharField(null=True, blank=True, max_length=32)
    mchid = models.CharField(null=True, blank=True, max_length=16)
    prepay_id = models.CharField(null=True, blank=True, max_length=64, unique=True, verbose_name='支付唯一订单号')
    code_url = models.CharField(null=True, blank=True, max_length=100, verbose_name='二维码地址')
    nonce_str = models.CharField(null=True, blank=True, max_length=32, verbose_name='随机字符串')

    class Meta:
        verbose_name = '微信订单'
        verbose_name_plural = verbose_name
        ordering = ('-created_time',)


