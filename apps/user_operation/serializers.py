"""
@author:zyf
@time:2019/09/05
@filename:seralizers.py
"""
from rest_framework import serializers


class OpenIdSerializers(serializers.Serializer):
    openid = serializers.CharField()
