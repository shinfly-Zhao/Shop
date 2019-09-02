"""
@author:zyf
@time:2019/09/02
@filename:xb_HTTPCODE.py
"""
from enum import Enum
from rest_framework.response import Response
class ResponseSatatusCode(Enum):
    HTTPCODE_1_OK = 1  # 返回成功并且有数据返回
    HTTPCODE_0_OK = 0  # 返回成功但无数据返回
    HTTPCODE_1001_PARAMETER_ERROR = 1001  # 参数错误
    HTTPCODE_1002_NOPOSTDATA = 1002  # 没有POST数据
    HTTPCODE_1003_CAN_NO_FIND = 1003  # 找不到资源
    HTTPCODE_1004_NO_PERMISSIONS = 1004  # 没有权限
    HTTPCODE_1005_SERVER_ERROR = 1005  # 服务器内部问题
    HTTPCODE_1006_PARAMETER_VALUE_ERROR = 1006  # 参数值错误
    HTTPCODE_1007_INCORRECT_CREDENTIALS = 1007  # 无效的凭证（账号不存在）
    HTTPCODE_2001_CREATED = 2001  # 创建成功
    HTTPCODE_2004_NO_CONTENT = 2004  # 成功接收处理


def CodeStatus(type, data):
    if type == "get":
        if data:
            return Response(data={
                "status": {
                    "code": ResponseSatatusCode.HTTPCODE_1_OK.value,
                    "msg": "success"
                },
                "data": data
            })
        else:
            return Response(data={
                "status": {
                    "code": ResponseSatatusCode.HTTPCODE_0_OK.value,
                    "msg": "nodata"
                },
            })