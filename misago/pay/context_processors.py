from django.urls import reverse


def pay_links(request):

    request.frontend_context.update({
        'PAY_WECHATPAY_QRCODE_API': reverse('misago:api:wechatpay-qrcode'),
        'PAY_WECHATPAY_STATUS_API': reverse('misago:api:wechatpay-status'),
    })

    return {}
