"""
@author:zyf
@time:2020/01/11
@filename:adminx.py
"""


import xadmin
from .models import *


class BaseChatXadmin():
    list_display = ['title', "user", "is_top", "is_use", "add_time", "get_twonums"]
    list_editable = ["is_top", "is_use"]
    list_filter = ["title"]
    model_icon = 'fa fa-user-plus'


class ReplayBaseChatXadmin():
    list_display = ['title', "user", "chat"]
    list_filter = ["title"]
    model_icon = "fa fa-wechat"


class UserFavChatXadmin():
    list_display = ['chat',"user"]
    model_icon = "fa fa-hand-peace-o"


xadmin.site.register(BaseChat,BaseChatXadmin)
xadmin.site.register(RreplyBasChat, ReplayBaseChatXadmin)
xadmin.site.register(UserChatFav,UserFavChatXadmin)