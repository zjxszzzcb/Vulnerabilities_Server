from django.db import models
from apps.role.models import Role

# 用户表
class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    username = models.CharField(max_length=50, verbose_name='用户名')
    password = models.CharField(max_length=36, verbose_name='密码')
    phone = models.CharField(max_length=50, verbose_name='电话')
    avatar = models.CharField(max_length=255, verbose_name='头像')
    sex = models.CharField(max_length=20, verbose_name='性别')
    email = models.CharField(max_length=20, verbose_name='邮箱')
    status = models.BooleanField(verbose_name='封禁')
    role = models.ForeignKey(Role, to_field="id", on_delete=models.CASCADE)
    remarks = models.TextField(verbose_name='描述')

    class Meta:
        db_table = "sys_user"