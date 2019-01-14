from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from wechatpy.exceptions import WeChatPayException

from misago.core.utils import get_logger
from misago.conf import settings
from .utils import (
    wechatpay_client, dict_to_xml, gen_out_trade_no, is_out_trade_no)
from .models import Order

logger = get_logger(__file__)


@api_view(['GET'])
def wechatpay_qrcode(request):
    body = "悬赏金支付"
    reward = int(request.GET.get('reward'))
    out_trade_no = gen_out_trade_no(wechatpay_client.mch_id)
    try:
        order = wechatpay_client.order.create(trade_type='NATIVE', out_trade_no=out_trade_no, body=body,
                                              total_fee=reward,
                                              notify_url=settings.WECHAT_CALLBACK_URL)
        obj = Order.objects.create(user=request.user,
                                   body=body,
                                   total_fee=reward,
                                   product_id='',
                                   notify_url=settings.WECHAT_CALLBACK_URL,
                                   out_trade_no=out_trade_no,
                                   status=Order.NOT_PAY,
                                   trade_type='NATIVE',
                                   appid=order.get('appid'),
                                   mchid=order.get('mch_id'),
                                   prepay_id=order.get('prepay_id'),
                                   code_url=order.get('code_url'),
                                   nonce_str=order.get('nonce_str'))
        logger.info("qr code out_trade_no: " + obj.out_trade_no)

    except Exception as e:
        raise WeChatPayException(return_msg=e.args[0])
    return Response({
        'code_url': order.get('code_url'),
        'out_trade_no': out_trade_no
    })


@csrf_exempt
def wechat_callback(request):
    cb_data = wechatpay_client.parse_payment_result(request.body)
    logger.info('callback result data: {}'.format(cb_data))
    if wechatpay_client.check_signature(cb_data):
        if cb_data.get('result_code') == 'SUCCESS':
            Order.objects.update_or_create(out_trade_no=cb_data.get('out_trade_no'),
                                           defaults=dict(
                                               transaction_id=cb_data.get('transaction_id'),
                                               nonce_str=cb_data.get('nonce_str'),
                                               pay_time=timezone.now(),
                                               status=Order.SUCCESS
                                           ))
            return HttpResponse(dict_to_xml({
                'return_code': 'SUCCESS',
                'return_msg': 'OK'
            }))
        else:
            Order.objects.update_or_create(out_trade_no=cb_data.get('out_trade_no'),
                                           defaults=dict(
                                               transaction_id=cb_data.get('transaction_id'),
                                               nonce_str=cb_data.get('nonce_str'),
                                               pay_time=timezone.now(),
                                               status=Order.PAY_ERROR
                                           ))
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
    return Response("bad signature", status=status.HTTP_400_BAD_REQUEST)

@login_required
@csrf_exempt
@api_view(['GET'])
def query_status(request):
    out_trade_no = str(request.GET.get('out_trade_no', ''))
    if is_out_trade_no(out_trade_no):
        objs = Order.objects.filter(user=request.user, out_trade_no=out_trade_no, deleted=False)
        if objs:
            obj = objs[0]
            return Response({
                'status': obj.status
            })
    raise WeChatPayException(return_code=-1, errmsg='bad out_trade_no!')
