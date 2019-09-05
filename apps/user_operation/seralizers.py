"""
@author:zyf
@time:2019/09/05
@filename:seralizers.py
"""

from rest_framework import serializers
from .models import *
from goods.seralizers import GoodsListSerializer
from rest_framework.validators import UniqueTogetherValidator


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsListSerializer()
    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default = serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav

        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
            )
        ]
        fields = ("user","goods",'id')  #  id 删除用
