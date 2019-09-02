"""
@author:zyf
@time:2019/09/02
@filename:xb_Response.py
"""
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from .xb_HTTPCODE import CodeStatus


class XB_ListModelMixin(viewsets.GenericViewSet,
                        mixins.ListModelMixin):

    def list(self, request, *args, **kwargs):
        method = self.request.META["REQUEST_METHOD"].lower()

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # return CodeStatus(type=method,data=serializer.data)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return CodeStatus(type=method,data=serializer.data)

class XB_ListModelMixin(viewsets.GenericViewSet,
                        mixins.ListModelMixin):

    def list(self, request, *args, **kwargs):
        method = self.request.META["REQUEST_METHOD"].lower()

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # return CodeStatus(type=method,data=serializer.data)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return CodeStatus(type=method,data=serializer.data)


class XB_RetrieveModelMixin(viewsets.GenericViewSet,
          mixins.RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        # path_id = self.request.META["PATH_INFO"].split("/")[2]
        # print(path_id)
        method = self.request.META["REQUEST_METHOD"].lower()
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CodeStatus(type=method, data=serializer.data)

