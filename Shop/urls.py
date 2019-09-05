"""Shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework.documentation import include_docs_urls  # 文档
import xadmin
from django.views.static import serve
from Shop.settings import MEDIA_ROOT,STATIC_ROOT
from rest_framework.routers import DefaultRouter
from goods.views import *
from users.views import *
from user_operation.views import *
from rest_framework_jwt.views import obtain_jwt_token
router = DefaultRouter()
router.register("categorys",GoodsCategoryViewSet,base_name="categorys")  # 配置商品分类的url
router.register("goods",GoodsViewSet,base_name="goods")  # 商品url
router.register("code",SmsCodeViewSet,base_name="code")  # 短信验证码
router.register("reg",UserRegistViewSet,base_name="reg")  # 短信验证码
router.register("userfavs",UserFavViewset,base_name="userfavs")  # 配置用户收藏

from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title="我的docs")
urlpatterns = [
    url(r'^shopdocs/', include_docs_urls(title='购物商品API')),
    url(r'^swagger/', schema_view),
    path('xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),  # 媒体文件
    url(r'^static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),  # 静态文件
    url(r'^', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('login/',obtain_jwt_token),
]
