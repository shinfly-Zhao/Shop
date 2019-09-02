"""
@author:zyf
@time:2019/08/23
@filename:seralizers.py
"""
from rest_framework import serializers
from .models import *


class GoodsCategorySerializer3(serializers.ModelSerializer):
    """
    商品类别信息序列化
    """
    class Meta:
        model = GoodsCategory
        fields = ('id', "name", "sub_cat")

class GoodsCategorySerializer2(serializers.ModelSerializer):
    """
    商品类别信息序列化
    """
    sub_cat = GoodsCategorySerializer3(many=True) # 数据库中设计 related_name="sub_cat"
    class Meta:
        model = GoodsCategory
        fields = ('id', "name", "sub_cat")




class GoodsCategorySerializer(serializers.ModelSerializer):
    """
    商品类别信息序列化
    """
    sub_cat = GoodsCategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = ('id', "name","sub_cat")
        # fields = "__all__"


class GoodsListSerializer(serializers.ModelSerializer):
    """
    商品列表序列化
    """
    # category = GoodsCategorySerializer()  # 用于显示外键信息  自定义 覆盖
    # images = GoodsImagesSerializer(many=True)
    class Meta:
        model = Goods
        fields = ('id', 'name', 'fav_num', 'sold_num', 'market_price', 'market_price')

class GoodsImagesSerializer(serializers.ModelSerializer):
    """
    商品小轮播
    """
    class Meta:
        model = GoodsImage
        fields = ("image",)

class GoodsRetrieveSerializer(serializers.ModelSerializer):
    """
    商品详情序列化
    """
    # category = GoodsCategorySerializer()  # 用于显示外键信息  自定义 覆盖
    images = GoodsImagesSerializer(many=True) # 轮播图片
    class Meta:
        model = Goods
        fields = ('id', 'name', 'fav_num', 'sold_num', 'market_price', 'market_price',"images")
