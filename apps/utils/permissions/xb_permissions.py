"""
@author:zyf
@time:2019/09/05
@filename:permissions.py
"""
# 公共权限验证
from rest_framework import permissions
from users.models import Merchants


class IsAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    用户自己相关 / 公共 信息
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # ('GET', 'HEAD', 'OPTIONS') 允许所有用户访问
        if request.method in permissions.SAFE_METHODS:
            return True

        # 否则只有当前用户可以修改编辑对象
        return obj.user == request.user


class UserHasMobile(permissions.BasePermission):
    # 查看用户是否绑定电话号码
    def has_object_permission(self, request, view, obj):
        if request.user.mobile:
            return True
        else:
            return False


class UserIsAdminOrXadmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.utype == "admin":
            return True
        else:
            return False


class BaseUrlPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return False

    # def has_object_permission(self, request, view, obj):
    #     """
    #     Return `True` if permission is granted, `False` otherwise.
    #     """
    #     return True
    # 判断商户门店号是否有效(基本)
    def has_object_permission(self, request, view, obj):
        return True
        # try:
        #     path = request.META["PATH_INFO"].strip("")
        #     pathList = path.split("/")
        #     shopId = pathList[1]
        #     shop = Merchants.objects.filter(number =int(shopId))
        #     if shop:
        #         return True
        #     else:
        #         return False
        # except:
        #     return False

