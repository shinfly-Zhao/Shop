from django.shortcuts import render
from utils.http.XBAPIView import *
from .models import *
from utils.permissions.permissions import *
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from .serializers import *
from rest_framework_xml.parsers import XMLParser
from rest_framework.views import APIView
from rest_framework import status
from utils.pay.wx.xcu import Openid
from utils.page.page import NewPageSetPagination,StatusPageSetPagination
from utils.pay.wx.xcu import WXPay
from utils.pay.wx.printer import PrinterUtils
from utils.permissions.xb_authentication import XBJSONWebTokenAuthentication
from utils.http.XBHTTPCode import ResponseSatatusCode


# 微信返回的信息为xml
class WechatPaymentXMLParser(XMLParser):
    media_type = 'text/xml'


class ShoppingCartViewSet(XBModelViewSet):
    """
    list:
        获取购物车详情
    create:
        加入购物车
    delete:
        删除购物记录
    update:
        更新购物记录
    """
    permission_classes = [IsAuthenticated, IsOnlyMyselfCan]
    authentication_classes = [XBJSONWebTokenAuthentication,SessionAuthentication]
    serializer_class = ShopCartListSerializer
    pagination_class = StatusPageSetPagination

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'create':
            return ShopCartCreateSerializer
        elif self.action == "update":
            return ShopCartUpdateSerializers
        else:
            return ShopCartListSerializer


# ----------------------------------订单支付相关---------------------------------


class WxPay(XBCreateModelMixin):
    # 支付
    permission_classes = [IsAuthenticated]
    serializer_class = PayOrederSerializer
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def create(self, request, *args, **kwargs):
        method = self.request.META["REQUEST_METHOD"].lower()
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return CodeStatus(type=method, data=serializer.data["paydata"], header=headers)
        except:
            return Response(error_msg(serializer._errors), status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        data = serializer.save()


class OredrViewSet(XBModelViewSet):
    # 订单相关
    permission_classes = [IsAuthenticated]
    authentication_classes = [XBJSONWebTokenAuthentication, SessionAuthentication]
    pagination_class = StatusPageSetPagination

    def get_queryset(self):
        # 返回当前用户的订单信息
        return OrderInfo.objects.filter(user=self.request.user.id)

    def get_serializer_class(self):

        if self.action == "list":
            return PayOrederListSerializer
        elif self.action == "create":
            return CreateOrederSerializer
        elif self.action == "update":
            return PayOrederUpdateSerializer

    def perform_create(self, serializer):
        # 创建订单
        order = serializer.save()
        # 创建订单详情
        if order.cart:
            # 购物车下单
            carts = order.cart.split("-")
            for cart in carts:
                car = ShoppingCart.objects.get(id=int(cart))
                order_goods = OrderGoods()
                order_goods.goods = car.goods.id
                order_goods.goods_num = car.nums
                order_goods.order = order.id
                order_goods.save()
                # car.delete()  # 购物车数据待删除
        else:
            # 直接下单的
            order_goods = OrderGoods()
            ids = order.goodsid.split("-")
            nums = order.nums.split("-")
            for id, num in zip(ids, nums):
                goods = Goods.objects.get(id=int(id))
                order_goods.goods = goods.id
                order_goods.goods_num = int(num)
                order_goods.order = order.id
                order_goods.save()


class GetWxCode(APIView):
    # 微信异步通知
    parser_classes = [WechatPaymentXMLParser]

    def post(self, request):
        # 微信异步通知支付结果  -- 修改状态为已付款
        postdata = self.request.data
        if postdata["return_code"] and postdata["result_code"] == "SUCCESS":
            # 这是支付
            out_trade_no = postdata["out_trade_no"]
            transaction_id = postdata["transaction_id"]
            order = OrderInfo.objects.get(order_sn=out_trade_no)
            if order:
                order.trade_no = transaction_id
                order.pay_status = "TRADE_SEND"
                order.save()
                # 打印订单
                code  = PrinterUtils().xbprint(order_id=order.id)
                if not code:
                    # 打印成功 返回0
                    pass
                else:
                    # 打印失败
                    pass
        # elif postdata["return_code"] == "SUCCESS":

        data = "<xml><return_code><![CDATA[SUCCESS]]>\
               </return_code><return_msg><![CDATA[OK]]></return_msg></xml>"
        return Response(data, content_type="text/xml")

    def get(self, request):
        data = "<xml><return_code><![CDATA[SUCCESS]]>\
                       </return_code><return_msg><![CDATA[OK]]></return_msg></xml>"
        return Response(data, content_type="text/xml")


class PutPayCode(APIView):
    """
    put:
        微信客户端修改订单状态
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    serializer_class = OrderPutSerializer

    def put(self, request):
        try:
            order_sn = self.request.data["order_sn"]
            msg = self.request.data["msg"]
            if msg in ["TRADE_SUCCESS", "TRADE_CLOSED", "WAIT_BUYER_PAY",
                       "TRADE_FINISHED", "PAYING"]:
                Order = OrderInfo.objects.filter(order_sn=order_sn, user=self.request.user)
                if Order:
                    Order[0].pay_status = msg
                    Order[0].save()
                    return Response(status=status.HTTP_200_OK, data={
                        "status": {
                            "code": ResponseSatatusCode.HTTPCODE_1_OK.value,
                            "msg": "success"
                        }})
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={
                        "status": {
                            "code": ResponseSatatusCode.HTTPCODE_4004_CAN_NO_FIND.value,
                            "msg": "找不到"
                        }})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={
                    "status": {
                        "code": ResponseSatatusCode.HTTPCODE_1006_PARAMETER_VALUE_ERROR.value,
                        "msg": ["TRADE_SUCCESS", "TRADE_CLOSED", "WAIT_BUYER_PAY",
                                "TRADE_FINISHED", "PAYING"]
                    }})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "status": {
                    "code": ResponseSatatusCode.HTTPCODE_1001_PARAMETER_ERROR.value,
                    "msg": "参数错误"
                }})





