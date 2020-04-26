"""
@author:zyf
@time:2020/01/08
@filename:adminx.py
"""

import xadmin
from xadmin import views
from .models import *
from django.contrib.auth.models import User
from xadmin.plugins.auth import UserAdmin


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "SignleShop管理"
    site_footer = "SignleShop管理"
    menu_style = "accordion"
    apps_icons = {"goods": "fa fa-television",
                  "trade": "fa fa-paypal",

                  'chat': 'fa fa-wechat',

                  }

class PartnerXadmin():
    list_display = ["name", "phone", "address", "desc"]

    model_icon = "fa fa-venus-double"


class AddressXadmin():
    list_display = ["user"]
    model_icon = "fa fa-address-card"


class UserXadmin(UserAdmin):
    list_display = ["nick_name", "user_font_img", "utype",
                    "get_order_nums", "get_order_total", "get_address"]
    list_editable = ["utype"]
    readonly_fields = ["get_order_nums", "get_order_total", "get_address"]
class SJRZXADMIN():
    list_display = ["user","name","number","is_ok"]
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Partner, PartnerXadmin)
xadmin.site.register(UserAddress, AddressXadmin)
xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserXadmin)
xadmin.site.register(Merchants, SJRZXADMIN)
