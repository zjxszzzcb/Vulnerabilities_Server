from django.db import models

# 角色表
class Role(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    name = models.CharField(max_length=100, verbose_name='角色名称')
    level = models.IntegerField(verbose_name='等级')
    remarks = models.TextField(verbose_name='描述')
    
    class Meta:
        db_table = "sys_role"
