"""
@author:zyf
@time:2019/09/08
@filename:page.py
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination, CursorPagination
from rest_framework import status
from rest_framework.response  import Response
from collections import OrderedDict, namedtuple
from django.core.paginator import InvalidPage
from utils.permissions.xb_exceptions import NotFound


class PageSetPagination(PageNumberPagination):
    """
    分页处理
    """
    page_size_query_description = "每页记录"
    page_query_description = "页码"
    page_size = 2  # 前台可以自定义每页显示的数量
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 1000


class NewPageSetPagination(PageNumberPagination):
    """
    分页处理
    """
    page_size_query_description = "每页记录"
    page_query_description = "页码"
    page_size = 15  # 前台可以自定义每页显示的数量
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100



    def get_paginated_response(self, data):
        if data > 0:
            status = 1
        else:
            status = 0
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ("status",status),
            ("hint","yes")
        ]))


class StatusPageSetPagination(PageNumberPagination):
    """
    分页处理(包含封装)
    """
    page_size_query_description = "每页记录"
    page_query_description = "页码"
    page_size = 10  # 前台可以自定义每页显示的数量
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

    def get_paginated_response(self, data):
        if data:
            code = 1,
            msg = "success"
            return Response(
            {
                "status": {
                    "code": code[0],
                    "msg": msg
                },
                "data": OrderedDict([
                    ('count', self.page.paginator.count),
                    # ('next', self.get_next_link()),
                    # ('previous', self.get_previous_link()),
                    ('data', data),
                ])
            })
        else:
            code = 0,
            msg = "nodata"
            return Response(
                {
                    "status": {
                        "code": code[0],
                        "msg": msg
                    }

                })

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            # msg = self.invalid_page_message.format(
            #     page_number=page_number, message=str(exc)
            # )
            raise NotFound()

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = False

        self.request = request
        return list(self.page)

