from django.db import models
from datetime import datetime,timedelta
from DjangoUeditor.models import UEditorField


class GoodsCategory(models.Model):
    # 商品类别 (每个商户都可以自定义商品类别)
    merchant = models.IntegerField(verbose_name="所属商户", help_text="所属商户",default=0)
    name = models.CharField(max_length=30, verbose_name="类别名称", help_text="类别名称")
    index = models.IntegerField(verbose_name="展示顺序", default=0)
    icon = models.ImageField(upload_to="category/icon/", verbose_name="类别图标", help_text="类别图标", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now() + timedelta(hours=8) , verbose_name="创建时间", help_text="创建时间")

    class Meta:
        verbose_name = "商品类别管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品类设计(隶属与不同的类别-->隶属于不同的商家)
    """
    category = models.ForeignKey(GoodsCategory, verbose_name="商品类目", on_delete=models.CASCADE, related_name="goods",
                                 help_text="商品类目")
    name = models.CharField(max_length=100, verbose_name="商品名", help_text="商品名")
    merchant = models.IntegerField(verbose_name="所属商户", help_text="所属商户",null=True,blank=True)  # 可用于直接查询
    # 该选项会默认给商家赋值
    goods_sn = models.CharField(max_length=50, default="", verbose_name="商品唯一货号", help_text="商品唯一货号")
    goods_num = models.IntegerField(default=0, verbose_name="库存数", null=True, blank=True, help_text="库存数")
    market_price = models.FloatField(default=0, verbose_name="市场价格", help_text="市场价格")
    shop_price = models.FloatField(default=0, verbose_name="本店价格", help_text="本店价格")
    goods_front_image = models.ImageField(upload_to="goods/goods/images/", null=True, blank=True, verbose_name="封面图",
                                          help_text="封面图")
    is_down = models.BooleanField(default=False, verbose_name="是否下架", help_text="是否下架")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除", help_text="是否删除")
    add_time = models.DateTimeField(default=datetime.now() + timedelta(hours=8), verbose_name="添加时间", help_text="添加时间")

    def sell_nums(self):
        allnum = 0
        allOrderInfo = self.ordergoods_set.filter(goods=self)
        for orderinfo in allOrderInfo:
            allnum+=orderinfo.goods_num
        return allnum

    class Meta:
        verbose_name = '商品管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SingleShopNew(models.Model):
    # 公告管理
    title = models.CharField(max_length=100, verbose_name="标题", help_text="标题")
    is_show = models.BooleanField(default=False, verbose_name="是否展示", help_text="是否展示")
    merchant = models.IntegerField(verbose_name="所属商户", help_text="所属商户", null=True, blank=True)  # 可用于直接查询
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = '公告管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class GoodsImage(models.Model):
    """
    商品轮播图 -- 每个商品的小图
    """
    goods = models.ForeignKey(Goods, verbose_name="商品", related_name="images", on_delete=models.CASCADE, help_text="商品")
    image = models.ImageField(upload_to="goods/ming", verbose_name="图片", null=True, blank=True, help_text="图片")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    """
    首页轮播图,文本展示/商品展示
    """

    SHOW_TYPE = (
        (1, "首页轮播"),
        (2, "最新活动"),
    )
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE, help_text="商品")
    image = models.ImageField(upload_to='goods/banner/', verbose_name="轮播图片", help_text="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播顺序", help_text="轮播顺序")
    show_type = models.IntegerField(default=1, choices=SHOW_TYPE, verbose_name="展示控制", help_text="展示控制")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name