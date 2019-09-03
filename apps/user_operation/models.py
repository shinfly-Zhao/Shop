from django.db import models
from users.models import UserProfile
from goods.models import Goods
from datetime import datetime
# Create your models here.
class UserFav(models.Model):
    """
    用户商品收藏
    """
    user = models.ForeignKey(UserProfile, verbose_name="用户",on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name="商品", help_text="商品id",on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '用户商品收藏'
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")  # 一个数据只能收藏一次

    def __str__(self):
        return self.user.username
