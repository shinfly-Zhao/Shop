"""
@author:zyf
@time:2020/04/14
@filename:xb_authentication.py
"""

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import jwt
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework_jwt.settings import api_settings
from utils.permissions import xb_exceptions

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class XBJSONWebTokenAuthentication(JSONWebTokenAuthentication):
    # 后期维护自定义Token
    def authenticate(self, request):
        # 得到具体的token 进行校验
        jwt_value = self.get_jwt_value(request)
        ip = request.META["REMOTE_ADDR"]
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)  # 还原token的组成部分{}
        except jwt.ExpiredSignature:
            # 过期签名
            raise xb_exceptions.AuthenticationFailed("Signature has expired")
        except jwt.DecodeError:
            # 错误签名
            raise xb_exceptions.AuthenticationFailed("Error decoding signature")
        except jwt.InvalidTokenError:
            raise xb_exceptions.AuthenticationFailed("Error signature ")

        user = self.authenticate_credentials(payload)
        # if ip not in user.uip.split("#"):
        #     # 抛出异常 重新登陆获取新的Token
        #     raise xb_exceptions.AuthenticationFailed("Signature has expired")
        return (user, jwt_value)

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        User = get_user_model()
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user
