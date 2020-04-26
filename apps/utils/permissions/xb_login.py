"""
@author:zyf
@time:2020/04/14
@filename:xb_login.py
"""
from rest_framework_jwt.views import *
from rest_framework import status
from utils.http.XBHTTPCode import ResponseSatatusCode,error_msg
from Shop.settings import BASE_URL


def xb_jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义登陆返回数据
    """
    if user:
        return {

            "status": {
                "code": ResponseSatatusCode.HTTPCODE_1_OK.value,
                "msg": "success"
            },
            "data": {
                'token': token,
                "nick_name": user.nick_name,
                "user_font":user.user_font or BASE_URL + "/meida/user/font/sindleshop.png"
            }
        }
    else:
        return None


class XBObtainJSONWebToken(ObtainJSONWebToken):
    """
    自定义登陆
    """

    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = xb_jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(error_msg(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
