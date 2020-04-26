from .serializers import *
from .models import *
from utils.http.XBAPIView import *
from utils.page.page import NewPageSetPagination,StatusPageSetPagination
from utils.permissions.permissions import BaseUrlPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from .filters import *
from user_operation.serializers import *
from goods.serializers import *
from rest_framework.decorators import action


class GoodsCategoryViewSet(XBListModelMixin):
    """
    商品类别
    """
    serializer_class = GoodsCategoryListSerizlizer
    permission_classes = [BaseUrlPermission]

    def get_queryset(self):
        return GoodsCategory.objects.filter(merchant=self.merchant_id).order_by("index")


class NewsViewSet(XBListModelMixin):
    # 公告
    serializer_class = NewsListSeralizer
    permission_classes = [BaseUrlPermission]

    def get_queryset(self):
        return SingleShopNew.objects.filter(is_show=True, merchant=self.merchant_number)


class GoodsViewSet(XBListModelMixin,
                   XBRetrieveModelMixin):
    permission_classes = [BaseUrlPermission]
    pagination_class = StatusPageSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    # 对价格 名称做过滤
    filter_class = GoodsFilter
    # 对商品名称 商品简介以及商品类容做过滤
    # search_fields = ["name","goods_brief",""]

    def get_queryset(self):
        ids = self.request.query_params.get("ids", None)
        if ids:
            id = []
            for i in ids.split("-"):
                id.append(int(i))
            return Goods.objects.filter(id__in=id)
        else:

            return Goods.objects.filter(is_down=False, is_delete=False,merchant=self.merchant_number)

    def get_serializer_class(self):
        if self.action == "list":
            return GoodsListSerializer
        elif self.action == "retrieve":
            return GoodsRetrieveSerializer
