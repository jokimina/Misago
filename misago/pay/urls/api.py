from django.conf.urls import url

from misago.pay.api import gen_payment_url


urlpatterns = [
    url(r'^pay/wechat/qrurl$', gen_payment_url, name='gen_payment_url'),
]
