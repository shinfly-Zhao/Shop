"""
@author:zyf
@time:2020/01/13
@filename:serializers.py
"""

from rest_framework import serializers
from .models import *
from datetime import datetime, timedelta
from random import Random
from utils.pay.wx.xcu import WXPay
import time


class ShopCartListSerializer(serializers.ModelSerializer):
    # 购物车列表
    goods = serializers.SerializerMethodField()  # 购物车商品详情

    def get_goods(self, instance):
        goods_id = instance.goods
        good = Goods.objects.get(id=int(goods_id), is_down=False, is_delete=False)
        if good:
            is_use = 1
        else:
            good = Goods.objects.get(id=int(goods_id))
            is_use = 0
        return {
            "id": good.id,
            "name": good.name,
            "image": "/media/" + str(good.goods_front_image),
            "price": good.shop_price,
            "is_use": is_use
        }

    class Meta:
        model = ShoppingCart
        fields = ("id","goods", "nums")


class ShopCartCreateSerializer(serializers.Serializer):
    # 购物车数据增加
    id = serializers.IntegerField(read_only=True)
    good = serializers.SerializerMethodField(read_only=True)  # 购物车商品详情
    nums = serializers.IntegerField(required=True, label="数量", min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不能小于一",
                                        "required": "请选择购买数量"
                                    }, help_text="数量")
    # user = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )
    up_down = serializers.BooleanField(write_only=True)
    goods = serializers.IntegerField(required=True, label="商品id", help_text="商品id",write_only=True)

    def get_good(self, instance):
        goods_id = instance.goods
        good = Goods.objects.get(id=int(goods_id), is_down=False, is_delete=False)
        if good:
            is_use = 1
        else:
            good = Goods.objects.get(id=int(goods_id))
            is_use = 0
        return {
            "id": good.id,
            "name": good.name,
            "image": "/media/" + str(good.goods_front_image),
            "price": good.shop_price,
            "is_use": is_use
        }

    def create(self, validated_data):
        user = self.context["request"].user  # 当前用户
        nums = validated_data["nums"]  # 商品数量
        goods = validated_data["goods"]  # 商品id
        existed = ShoppingCart.objects.filter(user=user.id, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
            if existed.nums > 0:
                pass
            else:
                existed.nums = 0
                existed.save()
        else:
            validated_data["user"] = user.id
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def validate(self, attr):
        # 判断是增加还是减少商品数量
        if not attr["up_down"]:
            attr["nums"] = - attr["nums"]
        del attr["up_down"]

        # 校验商品的有效性
        if Goods.objects.filter(id=int(attr["goods"])):
            pass
        else:
            raise serializers.ValidationError("确保商品存在")

        return attr


class ShopCartUpdateSerializers(serializers.ModelSerializer):
    # 直接修改购物车数量
    nums = serializers.IntegerField(min_value=1)

    class Meta:
        model = ShoppingCart
        fields = ["nums"]


class OrderGoodsSeralizer(serializers.ModelSerializer):
    goods_front_image = serializers.SerializerMethodField()

    def get_goods_front_image(self, obj):
        return "/media/" + str(obj.goods_front_image)

    class Meta:
        model = Goods
        fields = ("id", "goods_front_image", "name", "shop_price")


class GoodsOrderInfo(serializers.ModelSerializer):
    goods = OrderGoodsSeralizer()

    class Meta:
        model = OrderGoods

        fields = ("goods", "goods_num")


class CreateOrederSerializer(serializers.ModelSerializer):
    # 用户创建订单
    class Meta:
        model = OrderInfo
        fields = ("id", "address", "cart", "nums", "goodsid", "post_script")

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["cart"] = validated_data.get("cart", None)
        order_mount = 0  # 订单总金额
        if validated_data["cart"]:
            # 购物车下单
            for cart in validated_data["cart"].split("-"):
                cart = ShoppingCart.objects.get(id=int(cart))
                # 查询具体商品
                good = Goods.objects.get(id=int(cart.goods))
                order_mount += cart.nums * good.shop_price
            validated_data["order_mount"] = order_mount
            validated_data["cart"] = "-".join(validated_data["cart"])
        else:
            # 直接下单 可以考虑多个商品id
            goods = validated_data["goodsid"].split("-")
            nums = validated_data["goodsid"].split("-")
            for gid, num in zip(goods, nums):
                goods = Goods.objects.get(id=int(gid))
                order_mount += goods.shop_price * int(num)
                validated_data["order_mount"] = order_mount

        # 订单创建时间
        validated_data["add_time"] = datetime.now() + timedelta(hours=8)
        # 订单所属用户
        validated_data["user"] = user.id
        order = OrderInfo.objects.create(**validated_data)
        return order

    def validate(self, attr):
        # 校验购物车
        user = self.context["request"].user
        # 判断是否购物车下单
        cart = attr.get("cart", None)        # 购物车集合
        goodsid = attr.get("goodsid", None)  # 商品集合

        # 校验收获地址
        address = UserAddress.objects.filter(id=attr["address"],user=user.id)
        if address:
            pass
        else:
            raise serializers.ValidationError("address error")
        if cart:
            # 购物车创建订单
            cart = cart.split("-")
            for car in cart:
                shop = ShoppingCart.objects.filter(id=int(car), user=user.id)
                if shop:
                    continue
                else:
                    raise serializers.ValidationError("cart error")
            return attr
        elif goodsid:
            # 直接商品创建订单
            goodsid = goodsid.split("-")
            nums = attr["nums"].split("-")
            if len(goodsid) == len(nums):
                pass
            else:
                raise serializers.ValidationError("Parameter error")

            for gid, num in zip(goodsid, nums):
                goods = Goods.objects.get(id=int(gid))
                if goods:
                    if isinstance(int(num), int) and int(num) > 0:
                        pass
                    else:
                        raise serializers.ValidationError("Parameter error")
                else:
                    raise serializers.ValidationError("Parameter error")
            return attr
        else:
            # 直接返回参数错误提示
            raise serializers.ValidationError("Parameter error")


class PayOrederSerializer(serializers.Serializer):
    # 支付
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    order = serializers.IntegerField(required=True, help_text="订单id")
    paydata = serializers.JSONField(read_only=True)
    openid = serializers.CharField()

    def generate_order_sn(self, uid):
        # 当前时间+userid+随机数
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(
            time_str=(datetime.now() + timedelta(hours=8)).strftime("%Y%m%d%H%M%S"),
            userid=uid,
            ranstr=random_ins.randint(10, 99))
        return order_sn

    def create(self, validated_data):
        user = self.context["request"].user  # 所属用户
        orderid = validated_data["order"]  # 订单地址
        ip = self.context["request"].META["HTTP_X_FORWARDED_FOR"]
        wx_pay = WXPay(openid=validated_data["openid"])
        out_trade_no = self.generate_order_sn(user.id)  # 随机订单号
        PayOrder = OrderInfo.objects.get(id=int(orderid))  # 当前订单
        total_fee = PayOrder.order_mount  # 总金额
        # 创建订单详情
        # 商品
        order_info = OrderGoods.objects.filter(order=PayOrder)
        body = False
        for good in order_info:
            mygood = Goods.objects.get(id=good.goods.id)
            if mygood:
                if body:
                    body += "-" + mygood.name
                else:
                    body = ""
                    body += mygood.name
            else:
                pass
        body = body.split("-")
        if len(body) > 2:
            body = "-".join(body[0:2])
            body = body + "等"
        else:
            body = "-".join(body)

        redata = wx_pay.pay(ip=ip, nonce_str=self.generate_order_sn(user.id), total_fee=int(total_fee * 100),
                            out_trade_no=out_trade_no, body=body)
        # 开始创建订单

        if redata["return_code"] == "SUCCESS" and redata["result_code"] == "SUCCESS":
            # 成功
            order_sn = out_trade_no
            PayOrder.order_sn = order_sn
            PayOrder.save()
        prepay_id = redata["prepay_id"]
        # 获取随机字符串
        nonceStr = redata["nonce_str"]
        timeStamp = str(int(time.time()))
        # 获取paySign签名，这个需要我们根据拿到的prepay_id和nonceStr进行计算签名
        paySign = wx_pay.get_paysign(prepay_id, nonceStr)
        redata["paySign"] = paySign
        redata["timeStamp"] = timeStamp
        paydata = {
            'timeStamp': timeStamp,
            'nonceStr': nonceStr,
            'package': prepay_id,
            'signType': 'MD5',
            'paySign': paySign,
            "out_trade_no": out_trade_no,
        }
        return {"paydata": paydata,
                "order": validated_data["order"],
                "openid": redata["openid"]}

    def validate_order(self, order):
        Order = OrderInfo.objects.filter(id=int(order), user=self.context["request"].user)
        if Order.exists() and not Order[0].trade_no:
            return order
        else:
            raise serializers.ValidationError("订单重复")


class OrderGoodsSeralizer(serializers.ModelSerializer):
    goods_front_image = serializers.SerializerMethodField()

    def get_goods_front_image(self, obj):
        return "/media/" + str(obj.goods_front_image)

    class Meta:
        model = Goods

        fields = ("id", "goods_front_image", "name", "shop_price")


class GoodsOrderInfo(serializers.ModelSerializer):
    goods = OrderGoodsSeralizer()

    class Meta:
        model = OrderGoods

        fields = ("goods", "goods_num")


class PayOrederListSerializer(serializers.ModelSerializer):
    # 订单列表
    id = serializers.IntegerField()
    order_mount = serializers.FloatField()
    pay_status = serializers.CharField()
    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    goods = serializers.SerializerMethodField()

    def get_goods(self,instance):
        # 商品详情 查看属于该订单的订单详情
        all_goods = OrderGoods.objects.filter(order = instance.id)
        data = []
        for orderfood in all_goods:
            good = Goods.objects.get(id=orderfood.id)
            data.append({
                "id":good.id ,
                "name":good.name,
                "price":good.shop_price,
                "num":orderfood.goods_num,
                "image":"/media/" + str(good.goods_front_image)
            })
        return data

    class Meta:
        model = OrderInfo
        fields = ["id", "pay_status", "add_time", "order_mount","goods"]


class RRRR(serializers.Serializer):
    id = serializers.IntegerField()


class PayOrederUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ["pay_status"]

    def update(self, instance, validated_data):
        instance.pay_status = validated_data["pay_status"]
        instance.save()
        return instance


class OrderPutSerializer(serializers.Serializer):
    # 微信客户端(小程序)修改订单状态 -- 微信前端发送请求
    order_sn = serializers.CharField()
    msg = serializers.ChoiceField(choices=(
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("TRADE_FINISHED", "交易结束"),
    ))


# 获取Openid
class OpenIdGetSerialoizers(serializers.Serializer):
    code = serializers.CharField()
