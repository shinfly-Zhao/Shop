"""
@author:zyf
@time:2020/03/04
@filename:printer.py
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
from SingleShop.settings import BASE_DIR
from random import Random
from datetime import datetime,timedelta
from trade.models import *
from equipment.models import *


class PrinterUtils():


    def xbprint(self,order_id):

        equipment = Equmang.objects.filter(is_use=True)
        if len(equipment) == 0:
            return 1
        else:
            equipment =equipment[0]
        order = OrderInfo.objects.get(id=int(order_id))
        if order:
            pass
        else:
            return 1

        number = equipment.number
        key = equipment.key
        page = equipment.page
        ename = equipment.name
        post_script = order.post_script
        time = order.add_time
        address = order.address
        phone = address.signer_mobile
        add = address.province + address.city + address.district +address.address
        pc = PS.objects.filter(is_use=True)[0].price
        allGoods = OrderGoods.objects.filter(order=order)
        zj = 0
        sf = order.order_mount
        # 优惠券
        yh = 0
        if order.oupons:
            yh = order.oupons.lines
        strs = "\r"
        for i in allGoods:
            strname = (i.goods.name)[0:6]
            strnum = "*" + str(i.goods_num)
            strprice = str((i.goods.shop_price) * (i.goods_num))
            zj += (i.goods.shop_price) * (i.goods_num)
            strs += strname
            for j in range(7 - len(strname)):
                strs += "--"
            strs += ">"
            strs += " " + strnum + "----->" + strprice + "\r"

        data = {
            "deviceNo": number,
            "key": key,
            "printContent":
"""
<CB>{ename}</CB>
<C>下单时间:{time}</C>
<C>*******************************</C>
 <B>备注：{post_script}</B>
<C>*******************************</C>
 商品          数量      价格
    {count}
--------------其他--------------
优惠:{yh}     
派送费：{pc}
--------------------------------
            总计: {zj}
            实付: {sf}
--------------------------------
地址：{address}
电话：{mobile}
--------------------------------
                """.format(post_script=post_script,ename=ename,count=strs, address=add, mobile=phone, pc=pc, yh=yh, zj=zj, sf=sf,
                           time=time.strftime("%Y-%m-%d %H:%M:%S")),
            "times":page
        }
        a = requests.post("http://open.printcenter.cn:8080/addOrder", data=data)
        return a.json()["responseCode"]

