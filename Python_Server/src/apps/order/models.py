from django.db import models

# 订单表
class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    user = models.CharField(max_length=50, verbose_name='用户信息')
    food = models.CharField(max_length=50, verbose_name='食物信息')
    num = models.IntegerField(verbose_name='数量')
    remarks = models.TextField(verbose_name='描述')

    class Meta:
        db_table = "sys_order"