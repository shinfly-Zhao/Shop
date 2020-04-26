"""
@author:zyf
@time:2020/04/10
@filename:yy_exceptions.py
"""
# 自定义异常信息
from rest_framework.exceptions import APIException
from rest_framework import status
from utils.http.XBHTTPCode import ResponseSatatusCode


class NotAuthenticated(APIException):
    # 未登陆状态
    status_code = status.HTTP_401_UNAUTHORIZED

    default_detail = {
                        "status": {
                            "code": ResponseSatatusCode.HTTPCODE_4001_UNAUTHORIZED.value,
                            "msg": 'not_authenticated'}
                    }
    # default_code = 'not_authenticated'


class PermissionDenied(APIException):
    # 用户没有权限
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
                        "status": {
                            "code": ResponseSatatusCode.HTTPCODE_4003_NO_PERMISSIONS.value,
                            "msg": 'permission_denied'}
                    }


class NotFound(APIException):
    # 未找到资源
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {
                        "status": {
                            "code": ResponseSatatusCode.HTTPCODE_4004_NO_FIND.value,
                            "msg": 'not_found'}
                    }


class NotFound(APIException):
    # 未找到资源
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {
                        "status": {
                            "code": ResponseSatatusCode.HTTPCODE_4004_NO_FIND.value,
                            "msg": 'not_found'}
                    }


class AuthenticationFailed(APIException):
    # Token异常
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, msg):
        self.detail = {"status": {
            "code": ResponseSatatusCode.HTTPCODE_4001_UNAUTHORIZED.value,
            "msg": msg
        }}