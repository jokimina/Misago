from django.db import models


class CacheVersion(models.Model):
    cache = models.CharField(max_length=128)
    version = models.PositiveIntegerField(default=0)


class BaseModel(models.Model):
    """
     基础模型
    """
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    deleted = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        abstract = True
