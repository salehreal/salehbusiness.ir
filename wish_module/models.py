from django.db import models
from product_module.models import ProductModel
from user_module.models import User


# Create your models here.

class WishModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name = "علاقه مندی"
        verbose_name_plural = "علاقه مندی ها"

class WishDetailModel(models.Model):
    wish = models.ForeignKey(WishModel, on_delete=models.CASCADE, verbose_name='علاقه مندی')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='محصول')
    def __str__(self):
        return f'{self.product.title} - {self.wish.user.username}'