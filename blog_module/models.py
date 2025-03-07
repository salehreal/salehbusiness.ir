from django.db import models
from user_module.models import User


# Create your models here.

class BlogModel(models.Model):
    image = models.ImageField(upload_to='blog', verbose_name="تصویر")
    title = models.CharField(max_length=300, verbose_name="عنوان")
    text = models.TextField(verbose_name="متن")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, editable=False, verbose_name="کاربر")
    date = models.DateTimeField(null=True, verbose_name="تاریخ")
    visited = models.IntegerField(default=0, verbose_name="بازدید")
    is_active = models.BooleanField(default=True, verbose_name="منتشر")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'


class CommentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    parent = models.ForeignKey('CommentModel', on_delete=models.CASCADE, verbose_name='والد', null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True, verbose_name="ایجاد شده در")
    text = models.TextField(verbose_name='متن کامنت')
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, verbose_name='مقاله', db_index=True)
    is_publish = models.BooleanField(default=False, verbose_name='منتشر')
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name = 'کامنت مقاله'
        verbose_name_plural = 'کامنت های مقاله'
