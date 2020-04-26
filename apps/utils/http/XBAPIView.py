"""
@author:zyf
@time:2019/09/02
@filename:xb_Response.py
"""
from rest_framework import mixins, viewsets
from .XBHTTPCode import CodeStatus
from utils.http.XBHTTPCode import error_msg
from rest_framework_jwt.views import *
from rest_framework import status
from utils.permissions import xb_exceptions
from users.models import Merchants


class XBGenericViewSet(viewsets.GenericViewSet):

    def initial_merchant(self, request):
        # 初始化商家信息
        try:
            self.merchant_number = int(request.META["PATH_INFO"].split("/")[1])  # 商家号
            self.merchant_id = Merchants.objects.get(number=self.merchant_number).id  # 商家id
            self.merchant = Merchants.objects.get(number=self.merchant_number)  # 商家对象
            # 初始化用户信息
            self.user = self.request.user
            self.uid = self.user.id
        except:
            # 该路由不用商家信息
            pass

        # 初始化用户信息
        try:
            user = self.request.user
            uid = user.id
        except:
            pass


    def permission_denied(self, request, message=None):
        """
        分抛权限类型
        """
        if request.authenticators and not request.successful_authenticator:
            raise xb_exceptions.NotAuthenticated()
        raise xb_exceptions.PermissionDenied(detail=message)

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        self.format_kwarg = self.get_format_suffix(**kwargs)

        # Perform content negotiation and store the accepted info on the request
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

        # Determine the API version, if versioning is in use.
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme

        # Ensure that the incoming request is permitted

        self.perform_authentication(request)
        self.check_permissions(request)
        self.check_throttles(request)
        self.initial_merchant(request)  # 初始化商家信息


class XBListModelMixin(XBGenericViewSet,
                       mixins.ListModelMixin):
    """
    资源列表 默认多列表

    """
    many = True

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=self.many)
        return CodeStatus(type="get", data=serializer.data)


class XBRetrieveModelMixin(XBGenericViewSet,
                           mixins.RetrieveModelMixin):
    """
    资源详情
    """

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return CodeStatus(type="get", data=serializer.data)
        except:
            raise xb_exceptions.NotFound()


class XBCreateModelMixin(XBGenericViewSet,
                         mixins.CreateModelMixin):
    """
    创建资源
    """

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return CodeStatus(type="post", data=serializer.data)
        except:
            return Response(error_msg(serializer._errors or "告知我"), status=status.HTTP_400_BAD_REQUEST)


class XBDestroyModelMixin(XBGenericViewSet,
                          mixins.DestroyModelMixin):
    """
    资源删除
    """

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            raise xb_exceptions.NotFound()

    def perform_destroy(self, instance):
        instance.delete()


class XBUpdateModelMixin(mixins.UpdateModelMixin,
                         XBGenericViewSet):
    # 修改资源
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            try:
                instance = self.get_object()
            except:
                raise xb_exceptions.NotFound()

            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return CodeStatus(type="put", data=serializer.data)

        except:
            return Response(error_msg(serializer._errors or "告知我"), status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class XBModelViewSet(XBListModelMixin,
                     XBCreateModelMixin,
                     XBRetrieveModelMixin,
                     XBDestroyModelMixin,
                     XBUpdateModelMixin):
    pass
