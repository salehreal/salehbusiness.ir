from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=20)
    active_code = models.CharField(max_length=10)
    token = models.CharField(max_length=100)
    province = models.CharField(max_length=100, verbose_name="کشور", null=True, blank=True)
    address = models.CharField(max_length=500, verbose_name="آدرس", null=True, blank=True)
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
