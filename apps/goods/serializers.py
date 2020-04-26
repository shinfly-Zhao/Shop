"""
@author:zyf
@time:2020/01/08
@filename:seralizer.py
"""

from rest_framework import serializers
from .models import *


class GoodsCategoryListSerizlizer(serializers.ModelSerializer):
    # 首页常规类别展示
    icon = serializers.SerializerMethodField()

    def get_icon(self,instance):
        return "/media/"+str(instance.icon)
    class Meta:
        model = GoodsCategory
        fields = ["id", "name", "icon"]


class NewsListSeralizer(serializers.ModelSerializer):
    # 公告序列化
    class Meta:
        model = SingleShopNew
        fields = ["title"]

class GoodsListSerializer(serializers.ModelSerializer):
    """
    商品列表序列化
    """

    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return "/media/" + str(obj.goods_front_image)

    class Meta:
        model = Goods
        fields = ('id', 'name', 'market_price', 'shop_price', "image")


class GoodsRetrieveSerializer(serializers.ModelSerializer):
    """
    商品详情序列化
    """
    # images = GoodsImagesSerializer(many=True)  # 轮播图片
    images = serializers.SerializerMethodField()

    def get_images(self, instance):
        images = []
        images.append("/media/" + str(instance.goods_front_image))
        return images

    class Meta:
        model = Goods
        fields = ('id', 'name', 'market_price', 'shop_price', "images")
