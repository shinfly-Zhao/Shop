"""
@author:zyf
@time:2020/01/09
@filename:seralizers.py
"""
import re
from rest_framework import serializers
from users.models import *
from datetime import datetime, timedelta
from utils.http.XBHTTPCode import *
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator
from Shop.settings import REGEX_MOBILE
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

class UserAddressListSerializer(serializers.ModelSerializer):
    # 收获地址列表
    class Meta:
        model = UserAddress

        fields = ("id", "signer_name", "signer_mobile", "province",
                  "city", "district", "address", "is_default")


class UserAddressCreateSerializer(serializers.ModelSerializer):
    # 创建收获地址
    add_time = serializers.DateTimeField(read_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserAddress
        fields = "__all__"

    def create(self, validate_data):
        # 创建地址
        if validate_data["is_default"]:
            # 如果是默认 其他地址就不是默认
            alluseradd = UserAddress.objects.filter(user=self.context["request"].user)
            if alluseradd:
                for add in alluseradd:
                    add.is_default = False
                    add.save()
            else:
                pass
        else:
            pass
        useraddress = UserAddress.objects.create(**validate_data)
        return useraddress


class UserAddressUpdateSerializer(serializers.ModelSerializer):
    # 修改收获地址
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserAddress
        fields = ("province", "user", "city", "district", "address", "signer_name", "signer_mobile", "is_default")


class UserWxRegSerializer(serializers.ModelSerializer):
    # (微信一键注册)
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,write_only=True,
                                     validators=[UniqueValidator(queryset=UserProfile.objects.all(), message="user existed")])
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def create(self, validated_data):
        user = super(UserWxRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self,instance):
        user = self.context["request"].user  # 当前用户
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    class Meta:
        model = UserProfile
        fields = ["username", "password","token","user_font","nick_name"]



class MobileBinding(serializers.ModelSerializer):
    # 限制用户的输入情况

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")

    def create(self, validated_data):
        user = self.context["request"].user
        user.mobile = validated_data["mobile"]
        user.save()
        return user

    def validate_code(self, code):

        # 检验验证码的正确性
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["mobile"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]  # 获取到最后一个验证码

            five_mintes_ago = datetime.now() - timedelta(hours=8, minutes=15, seconds=0)  # 5分钟之前的时间
            five_mintes_ago = five_mintes_ago.strftime("%Y-%m-%d-%H-%M")
            last = last_record.add_time.strftime("%Y-%m-%d-%H-%M")
            if five_mintes_ago > last:  # 前五分钟的时间如果大于真正注册的时间就当成过期
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        del attrs["code"]  # 删除验证码
        return attrs

    class Meta:
        model = UserProfile
        fields = ("user", "code", "mobile")


class SmsSerializer(serializers.Serializer):
    # 发送手机验证码 （用户输入电话号码 并发送验证码）
    mobile = serializers.CharField(max_length=11, help_text="电话号码")

    def validate_mobile(self, mobile):
        # 手机是否注册
        if UserProfile.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        # one_mintes_ago 表示一分钟之前的时间
        one_mintes_ago = datetime.now() - timedelta(minutes=1)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上次发送还未超过60s")
        return mobile


class UserUpdateInfo(serializers.Serializer):
    nick_name = serializers.CharField()
    user_font = serializers.CharField()

    def create(self, validate_data):
        user = self.context["request"].user
        user.nick_name = validate_data["nick_name"]
        user.user_font = validate_data["user_font"]
        user.save()
        return user


class PartnerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = "__all__"
