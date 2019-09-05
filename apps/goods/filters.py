"""
@author:zyf
@time:2019/9/5
@filename:filters.py
@Goods 过滤器
"""

import  django_filters
from .models import Goods
from django.db.models import Q


class GoodsFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(field_name="name",lookup_expr="icontains",help_text="商品名称")
    top_category = django_filters.NumberFilter(method="top_category_filter",help_text="商品所属类别id")  # 查找一类商品下的所有商品
    min = django_filters.NumberFilter(method="min_filter",help_text="商品市场/本店最低价格")
    max = django_filters.NumberFilter(method="max_filter",help_text="商品市场/本店最高价格")

    def min_filter(self,queryset, name, value):

        return queryset.filter(Q(shop_price__lte=value) | Q(market_price__lte=value))

    def max_filter(self,queryset, name, value):

        return queryset.filter(Q(shop_price__gte=value) | Q(market_price__gte=value))

    def top_category_filter(self, queryset, name, value):
        """
        :param queryset: 原始数据 来自 get_queryset()
        :param name: 参数名称 top_category
        :param value: 参数值
        :return: 返回符合结果的数据
        """
        return  queryset.filter(Q(category=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ["min","name","max"]