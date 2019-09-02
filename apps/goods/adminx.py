"""
@author:zyf
@time:2019/08/30
@filename:adminx.py
"""
from .models import *

import xadmin

class GoodsCateGoryXadmin():
    list_display = ["name","category_type"]

class GoodsXadmin():
    list_display = ["name", "goods_num","market_price","shop_price","goods_brief"]

class GoodsBannerXadmin():
    # 商品轮播小图序列化
    list_display = ["goods", "image"]

xadmin.site.register(GoodsCategory, GoodsCateGoryXadmin)
xadmin.site.register(Goods, GoodsXadmin)
xadmin.site.register(GoodsImage, GoodsBannerXadmin)