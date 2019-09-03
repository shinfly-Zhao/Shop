"""
@author:zyf
@time:2019/09/03
@filename:seralizer.py
"""
import re
from rest_framework import serializers
from users.models import UserProfile
from Shop.settings import REGEX_MOBILE
from datetime import datetime,timedelta
from users.models import VerifyCode
from utils.http.xb_HTTPCODE import ResponseSatatusCode
from rest_framework.validators import UniqueValidator

class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """

        # 手机是否注册
        if UserProfile.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError({
                "status": {
                    "code": ResponseSatatusCode.HTTPCODE_40002_RULES_ERROR.value,
                    "msg": "用户已村存在"
                },
            })

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError({
                "status": {
                    "code": ResponseSatatusCode.HTTPCODE_40002_RULES_ERROR.value,
                    "msg": "手机号码非法"
                },
            })

        # 验证码发送频率
        # one_mintes_ago 表示一分钟之前的时间
        one_mintes_ago = datetime.now() - timedelta(minutes=1)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError({
                "status": {
                    "code": ResponseSatatusCode.HTTPCODE_40002_RULES_ERROR.value,
                    "msg": "距离上一次发送未超过60s"
                },
            })
        return mobile

class UserRegSerializer(serializers.ModelSerializer):
    # 限制用户的输入情况
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4,label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=UserProfile.objects.all(), message="用户已经存在")])

    password = serializers.CharField(
        style={'input_type': 'password'},help_text="密码", label="密码", write_only=True,
    )
    repassword = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )



    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_code(self, code):

        # 检验验证码的正确性
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["mobile"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]  # 获取到最后一个验证码

            five_mintes_ago = datetime.now() - timedelta(hours=8, minutes=5, seconds=0)  # 5分钟之前的时间
            five_mintes_ago = five_mintes_ago.strftime("%Y-%m-%d-%H-%M" )
            last = last_record.add_time.strftime("%Y-%m-%d-%H-%M" )
            if five_mintes_ago >  last:  # 前五分钟的时间如果大于真正注册的时间就当成过期
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate_repassword(self, code):
        if self.initial_data["password"] != self.initial_data["repassword"]:
            raise serializers.ValidationError("密码不一致")
        # 检验验证码的正确性

    def validate(self, attrs):

        del attrs["code"]  # 删除验证码
        del attrs["repassword"]  # 删除确认密码

        return attrs

    class Meta:
        model = UserProfile
        # 返回的是用户名 验证码 手机号 密码
        # 但是用户表里面没有 code 所以最后会删除
        fields = ("username", "code", "mobile", "password","repassword")