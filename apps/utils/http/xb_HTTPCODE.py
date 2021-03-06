# """
# @author:zyf
# @time:2019/09/02
# @filename:xb_HTTPCODE.py
# """
# from enum import Enum
# from rest_framework.response import Response
#
#
# class ResponseSatatusCode(Enum):
#     HTTPCODE_1_OK = 1  # 返回成功并且有数据返回
#     HTTPCODE_0_OK = 0  # 返回成功但无数据返回
#     HTTPCODE_1001_PARAMETER_ERROR = 1001  # 参数错误
#     HTTPCODE_1002_NOPOSTDATA = 1002  # 没有POST数据
#     HTTPCODE_1003_CAN_NO_FIND = 1003  # 找不到资源
#     HTTPCODE_4003_NO_PERMISSIONS = 4003  # 没有权限
#     HTTPCODE_4004_NO_FIND = 4004  # 没有找到
#     HTTPCODE_4001_UNAUTHORIZED = 4001  # 状态失效
#     HTTPCODE_1005_SERVER_ERROR = 1005  # 服务器内部问题
#     HTTPCODE_1006_PARAMETER_VALUE_ERROR = 1006  # 参数值错误
#     HTTPCODE_1007_INCORRECT_CREDENTIALS = 1007  # 无效的凭证（账号不存在）
#     HTTPCODE_2001_CREATED = 2001  # 创建成功
#     HTTPCODE_2004_NO_CONTENT = 2004  # 成功接收处理
#     HTTPCODE_4000_BAD_REQUEST = 4000  # 请求失败
#     HTTPCODE_4029_THROTTLE = 4029  # 请求失败
#
#
# def CodeStatus(type, data,html=None,header=None):
#     if type == "get" or type =="update":
#         if data:
#             return Response(data={
#                 "status": {
#                     "code": ResponseSatatusCode.HTTPCODE_1_OK.value,
#                     "msg": "success"
#                 },
#                 "data": data
#             },template_name=html,headers=header)
#         else:
#             return Response(data={
#                 "status": {
#                     "code": ResponseSatatusCode.HTTPCODE_0_OK.value,
#                     "msg": "nodata"
#                 },
#             })
#     elif type == "post":
#         return Response(data={
#             "status": {
#                 "code": ResponseSatatusCode.HTTPCODE_2001_CREATED.value,
#                 "msg": "success"
#             },
#             "data": data
#         })
#
#
#
# def error_msg(msg):
#     return {"status": {
#                     "code": ResponseSatatusCode.HTTPCODE_40002_RULES_ERROR.value,
#                     "msg": msg
#                 }}