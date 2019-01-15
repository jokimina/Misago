from django.conf.urls import url

from misago.pay.api import (
    wechatpay_qrurl, wechatpay_callback, query_status, event_callback,
    wechat_binding_qrurl, query_bind_status
)


urlpatterns = [
    url(r'^pay/wechat/qrurl$', wechatpay_qrurl, name='wechatpay-qrurl'),
    url(r'^pay/wechat/callback$', wechatpay_callback, name="wechatpay-callback"),
    url(r'^pay/wechat/status$', query_status, name="wechatpay-status"),
    url(r'^pay/event/callback$', event_callback, name="wechat-event-callback"),
    url(r'^pay/bind/qrurl$', wechat_binding_qrurl, name="wechat-bind-qrurl"),
    url(r'^pay/bind/status$', query_bind_status, name="wechat-bind-status")
]
