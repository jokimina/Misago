from django.conf.urls import url

from misago.pay.api import (
    wechatpay_qrcode, wechat_callback, query_status
)


urlpatterns = [
    url(r'^pay/wechat/qrurl$', wechatpay_qrcode, name='wechatpay-qrcode'),
    url(r'^pay/wechat/callback$', wechat_callback, name="wechatpay-callback"),
    url(r'^pay/wechat/status$', query_status, name="wechatpay-status")
]
