from utils.http.XBAPIView import *
from .serializers import *
from utils.pay.wx.xcu import Openid


class OpenidViewSet(XBListModelMixin):
    serializer_class = OpenIdSerializers
    # 获取用户openid(用户注册或者微信登陆)
    many = False
    def get_queryset(self):

        code = self.request.query_params.get("code", 0)
        if code:
            data = Openid(code=code).openid()
            if data:
                return data
            else:
                None
        else:
            return None