from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import escape, format_html


class UserProfile(AbstractUser):
    """
    * 自定义用户(包括商户以及商户下的所有用户)
    """
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female",
                              verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    utype = models.CharField(default="members", max_length=50,
                             choices=(("members", "会员"), ("admin", "管理员"), ("merchants", "商家"), ("xadmin", "超级用户(内部)")),
                             verbose_name="用户类型")
    fuser = models.ForeignKey("self", null=True, related_name="chuser", blank=True,on_delete=models.DO_NOTHING)
    user_font = models.TextField(default="user/font/sindleshop.png", verbose_name="用户头像")
    nick_name = models.CharField(max_length=100, verbose_name="用户昵称", default="暂无昵称")
    add_time = models.DateTimeField(default=datetime.now() + timedelta(hours=8), verbose_name="注册时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def user_font_img(self):

        return format_html(
            '<img src="{}" style="width:30px;height:30px"/>',
            self.user_font,
        )

    user_font_img.short_description = u"微信头像"

    def get_order_nums(self):
        # 获取订单数
        return self.orderinfo_set.filter(user=self).count()

    get_order_nums.short_description = u"订单数"

    def get_order_total(self):
        # 获取订单金额
        total = 0
        allOrder = self.orderinfo_set.filter(user=self)
        for order in allOrder:
            total += order.order_mount
        return round(total, 3)

    get_order_total.short_description = u"订单金额"

    def get_address(self):
        # 获取订单金额
        add = ""
        addrsss = self.useraddress_set.filter(user=self, is_default=True)
        for addrs in addrsss:
            add += addrs.city + addrs.district + addrs.district
        return add

    get_address.short_description = u"默认地址"

    def __str__(self):
        return self.nick_name


class Merchants(models.Model):
    # * 商家认证信息
    user = models.ForeignKey(UserProfile, verbose_name="所属用户", on_delete=models.DO_NOTHING, related_name="merchants",
                             help_text="所属用户", null=True, blank=True)
    name = models.CharField(max_length=30, verbose_name="商家名称", help_text="商家名称")
    front_img = models.ImageField(verbose_name="商铺Logo", help_text="商铺Logo", upload_to="merchants/frontimg/")
    number = models.IntegerField(verbose_name="商铺号",help_text="商铺号")
    is_ok = models.BooleanField(default=False, verbose_name="是否通过")

    class Meta:
        verbose_name = "商家认证管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserAddress(models.Model):
    """
    * 用户收货地址
    """
    user = models.IntegerField(default=0, verbose_name="所属用户")
    province = models.CharField(max_length=100, verbose_name="省份", help_text="省份")
    city = models.CharField(max_length=100, verbose_name="城市", help_text="城市")
    district = models.CharField(max_length=100, verbose_name="区域", help_text="区域")
    address = models.CharField(max_length=100, verbose_name="详细地址", help_text="详细地址")
    signer_name = models.CharField(max_length=100, verbose_name="签收人", help_text="签收人")
    signer_mobile = models.CharField(max_length=11, verbose_name="电话", help_text="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    is_default = models.BooleanField(default=False, verbose_name="是否默认")

    class Meta:
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class Partner(models.Model):
    name = models.CharField(verbose_name="名称", max_length=100)
    phone = models.CharField(verbose_name="联系方式", max_length=11)
    address = models.CharField(verbose_name="所在城市", max_length=100)
    desc = models.CharField(verbose_name="个人介绍", max_length=500)

    class Meta:
        verbose_name = "合伙人管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
