from wechatpy.pay import WeChatPay
from misago.conf import settings

import time
import random
from datetime import datetime


def create_wechatpay_client():
    return WeChatPay(settings.WECHAT_APP_ID, settings.WECHAT_API_KEY,settings.WECHAT_MCH_ID)


def dict_to_xml(d):
    xml = ['<xml>\n']
    for k, v in d.items():
        xml.append(
            '<{0}><![CDATA[{1}]]></{0}>\n'.format(k, v)
        )
    xml.append('</xml>')
    return ''.join(xml)


def is_out_trade_no(d):
    return len(d) == 28 and d[:10] == settings.WECHAT_MCH_ID


def gen_out_trade_no(mch_id):
    now = datetime.fromtimestamp(time.time())
    return '{0}{1}{2}'.format(
                mch_id,
                now.strftime('%Y%m%d%H%M%S'),
                random.randint(1000, 10000)
            )

wechatpay_client = create_wechatpay_client()
