from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from .seralizer import *
from random import choice
from utils.mobile_code.YunPian import YunPian
from Shop.settings import MPBILEAPIKEY
from rest_framework import status
from users.models import VerifyCode
from utils.http.xb_HTTPCODE import ResponseSatatusCode
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class SmsCodeViewSet(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(MPBILEAPIKEY)
        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:

            return Response(status=status.HTTP_400_BAD_REQUEST,data={
                "status": {
                    "code": ResponseSatatusCode.HTTPCODE_40001_NO_CONTENT.value,
                    "msg": sms_status["msg"]
                }
            })
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response(status=status.HTTP_201_CREATED,data={
                "status": {
                    "code": ResponseSatatusCode.HTTPCODE_2001_CREATED.value,
                    "msg": "success"
                }
            })


class UserRegistViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin):
    """
    用户注册
    """
    # permission_classes = (IsAuthenticated,)  # 要求用户登录
    serializer_class = UserRegSerializer
    queryset = UserProfile.objects.all()
    # authentication_classes = (JSONWebTokenAuthentication,)  # 指定何种方式进行用户身份的认证

    # def get_permissions(self):
    #     if self.action == "retrieve":
    #         return [permissions.IsAuthenticated()]
    #     elif self.action == "create":
    #         return []
    #     return []

    def get_serializer_class(self):
        # if self.action == "retrieve":
        #     return UserDetailSerializer
        if self.action == "create":
            return UserRegSerializer
        # return UserDetailSerializer
    #
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        # re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)
    #
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()