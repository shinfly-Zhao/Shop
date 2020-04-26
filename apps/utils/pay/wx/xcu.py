"""
@author:zyf
@time:2019/09/29
@filename:xcu.py
"""

import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append("/home/admin/AllProject/PythonWeb/SingleShop")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SingleShop.settings")
import django

django.setup()
import hashlib
import xmltodict
import time
import os
import requests
from Shop.settings import BASE_DIR,WXXCX_SETTING
from random import Random
from datetime import datetime, timedelta
from trade.models import *


class WXPay():
    def __init__(self, openid=None):
        self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        self.openid = openid
        self.mch_id = "1576083821"  # 商户号
        self.appid = "wx71231d014dbe202a"
        self.key = "qingshuru32gezifuzhiyunxu1234567"
        self.backurl = "https://api.mch.weixin.qq.com/secapi/pay/refund"

    # 支付
    def pay(self, ip, nonce_str, total_fee, out_trade_no,body):
        data = {
            "appid": self.appid,  # 小程序ID
            "mch_id": self.mch_id,  # 商户号
            "nonce_str": nonce_str,  # 随机字符串
            "body": body,  # 商品描述
            "out_trade_no": out_trade_no,  # 商户订单号
            "total_fee": total_fee,  # 标价金额
            "spbill_create_ip": ip,  # 终端IP
            "notify_url": "https://api.zbaigu.com/getpay/",  # 通知地址
            "trade_type": "JSAPI",  # 交易类型
            "openid": self.openid  # 用户openid
        }

        stringA = '&'.join(["{0}={1}".format(k, data.get(k)) for k in sorted(data)])
        stringSignTemp = '{0}&key={1}'.format(stringA, self.key)
        sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
        data["sign"] = sign.upper()

        xml = []
        for k in sorted(data.keys()):
            v = data.get(k)
            if k == 'detail' and not v.startswith('<![CDATA['):
                v = '<![CDATA[{}]]>'.format(v)
            xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
        xml = '<xml>{}</xml>'.format(''.join(xml))
        response = requests.post(self.url, data=xml.encode('utf-8'))
        redata = response.content

        wx_redata = dict(xmltodict.parse(redata, encoding="utf-8"))
        wx_redata["xml"]["openid"] = self.openid

        return wx_redata["xml"]

    def get_paysign(self, prepay_id, nonceStr):
        # 返回给小程序
        pay_data = {
            'appId': self.appid,
            'nonceStr': nonceStr,
            'package': "prepay_id=" + prepay_id,
            'signType': 'MD5',
            'timeStamp': str(int(time.time()))
        }

        stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k)) for k in sorted(pay_data)])
        stringSignTemp = '{0}&key={1}'.format(stringA, self.key)
        sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
        return sign.upper()  # 返回给小程序的签名

    def back(self, out_trade_no, nonce_str, out_refund_no, total_fee, refund_fee):
        data = {
            "appid": self.appid,  # 小程序ID
            "mch_id": self.mch_id,  # 商户号
            "nonce_str": nonce_str,  # 随机字符串
            "out_trade_no": out_trade_no,  # 商户订单号
            "total_fee": total_fee,  # 订单金额
            "out_refund_no": out_refund_no,  # 商户退款单号
            "refund_fee": refund_fee,  # 退款金额
        }

        stringA = '&'.join(["{0}={1}".format(k, data.get(k)) for k in sorted(data)])
        stringSignTemp = '{0}&key={1}'.format(stringA, self.key)
        sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
        data["sign"] = sign.upper()

        xml = []
        for k in sorted(data.keys()):
            v = data.get(k)
            if k == 'detail' and not v.startswith('<![CDATA['):
                v = '<![CDATA[{}]]>'.format(v)
            xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
        xml = '<xml>{}</xml>'.format(''.join(xml))
        ssh_keys_path = os.path.join(BASE_DIR, "apps", "utils", "permissions")
        weixinapiclient_cert = os.path.join(ssh_keys_path, "apiclient_cert.pem")
        weixinapiclient_key = os.path.join(ssh_keys_path, "apiclient_key.pem")
        headers = {'Content-Type': 'application/xml'}
        response = requests.post(self.backurl, data=xml, cert=(weixinapiclient_cert, weixinapiclient_key),
                                 headers=headers, verify=True)
        redata = response.content
        wx_redata = dict(xmltodict.parse(redata, encoding="utf-8"))
        return wx_redata["xml"]["return_code"]

    def generate_order_sn(self, uid):
        # 当前时间+userid+随机数
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(
            time_str=(datetime.now() + timedelta(hours=8)).strftime("%Y%m%d%H%M%S"),
            userid=uid,
            ranstr=random_ins.randint(10, 99))
        return order_sn


class Openid():
    def __init__(self, code):
        self.code = code

    def openid(self):
        urls = "https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code="+str(self.code)+"&grant_type=authorization_code".format(appid=WXXCX_SETTING["APPID"],secret=WXXCX_SETTING["SECRET"])
        data = requests.get(urls)
        data = data.json()
        return data



