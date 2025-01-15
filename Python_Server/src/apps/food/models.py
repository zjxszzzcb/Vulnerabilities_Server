from django.db import models
from apps.user.models import User

# 食物表
class Food(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    foodname = models.CharField(max_length=50, verbose_name='食物名称')
    user = models.ForeignKey(User, to_field="id", on_delete=models.CASCADE)
    foodicon = models.CharField(max_length=100, verbose_name='食物图标')
    foodprocedure = models.TextField(verbose_name='做菜步骤')
    video = models.CharField(max_length=100, verbose_name='视频')
    price = models.FloatField(verbose_name='价格')
    remarks = models.TextField(verbose_name='描述')

    class Meta:
        db_table = "sys_food"

