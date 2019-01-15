from django.urls import reverse


def pay_links(request):

    request.frontend_context.update({
        'PAY_WECHATPAY_QRCODE_API': reverse('misago:api:wechatpay-qrurl'),
        'PAY_WECHATPAY_STATUS_API': reverse('misago:api:wechatpay-status'),
        'PAY_WECHAT_BIND_QRCODE_API': reverse('misago:api:wechat-bind-qrurl'),
        'PAY_WECHAT_BIND_STATUS_API': reverse('misago:api:wechat-bind-status'),
    })

    return {}
