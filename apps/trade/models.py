from django.db import models
from goods.models import *
from users.models import UserProfile, UserAddress


class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.IntegerField(default=0, verbose_name="用户", help_text="所属用户")
    goods = models.IntegerField(default=0, verbose_name="商品", help_text="所属商品")
    nums = models.IntegerField(default=0, verbose_name="购买数量", help_text="商品数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")

    def __str__(self):
        return "添加成功"


class OrderInfo(models.Model):
    """
    订单
    """
    ORDER_STATUS = (
        (0, "待支付"),
        (1, "待发货"),
        (2, "已发货"),
        (3, "退款中"),
        (4, "已退款"),
        (5, "退款拒绝"),
    )

    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="订单号")
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name=u"交易号")
    pay_status = models.IntegerField(choices=ORDER_STATUS, default=0, verbose_name="订单状态")
    post_script = models.CharField(max_length=200, verbose_name="订单留言", null=True, blank=True)
    order_mount = models.FloatField(default=0.0, verbose_name="订单金额")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")
    cart = models.CharField(max_length=100, null=True, blank=True, verbose_name="购物车")
    goodsid = models.CharField(max_length=100, null=True, blank=True, verbose_name="商品")
    nums = models.CharField(max_length=100, null=True, blank=True, verbose_name="数量")

    # 用户信息
    user = models.IntegerField(verbose_name="v用户")
    address = models.IntegerField(verbose_name="收货地址", default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")

    class Meta:
        verbose_name = u"订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user)

    def go_to(self):
        from django.utils.safestring import mark_safe
        # mark_safe后就不会转义
        return mark_safe("<a href='https://zhaoyunfei.vip/message/'>跳转</a>")

    go_to.short_description = "跳转"


class OrderGoods(models.Model):
    """
    订单的商品详情
    """
    order = models.IntegerField(verbose_name="订单信息",default=0)
    goods = models.IntegerField(verbose_name="商品",default=0)
    goods_num = models.IntegerField(default=0, verbose_name="商品数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
