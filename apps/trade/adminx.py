"""
@author:zyf
@time:2020/02/17
@filename:adminx.py
"""
import os
import sys
from .models import *
import xadmin
from django.core.exceptions import PermissionDenied
# from utils.pay.wx.xcu import WXPay
from xadmin.plugins.actions import BaseActionView


class ShoppingCartAdmin():
    # 购物车
    list_display = ["user", "goods", "nums"]
    model_icon = "fa fa-cart-arrow-down"



class MyAction(BaseActionView): # 定义一个动作
    action_name = "MyAction"  # 动作名
    description = "参数化构建"  # 要显示的名字
    model_perm = "change"   # 该动作所需权限

    # def do_action(self, queryset):  # queryset 是包含了已经选择的数据的 queryset
    #     wx_pay = WXPay()
    #     for order in queryset:
    #
    #         out_refund_no = wx_pay.generate_order_sn(order.user.id)  # 随机退单号
    #         total_fee = order.order_mount  # 总金额
    #         redata = wx_pay.back(out_trade_no=order.order_sn, nonce_str=wx_pay.generate_order_sn(order.user.id),
    #                              out_refund_no=out_refund_no, total_fee=total_fee, refund_fee=total_fee)
    # # 退款成功


class OrderXadmin():
    list_display = ["user", "order_sn", "trade_no", "pay_status", "order_mount"]
    show_detail_fields = ['address']
    list_filter = ["pay_status","user"]
    # readonly_fields = ["pay_status"]
    # actions = [MyAction,]
    refresh_times = [3, 5]
    list_editable = ["pay_status"]
    model_icon = "fa fa-cc-paypal"


class OrderGoodsXadmin():
    list_display = ["order", "goods", "goods_num", "add_time"]
    list_filter = ["goods"]
    model_icon = "fa fa-gift"


xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderXadmin)
xadmin.site.register(OrderGoods, OrderGoodsXadmin)
