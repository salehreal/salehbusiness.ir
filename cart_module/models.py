from getpass import fallback_getpass

from django.db import models
from user_module.models import User
from product_module.models import ProductModel
# Create your models here.

class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده / نشده')
    payment_date = models.DateTimeField(null=True, verbose_name='تاریخ پرداخت')
    process = models.BooleanField(default=False, verbose_name='درحال پردازش')
    delivery = models.BooleanField(default=False, verbose_name='تحویل شده')
    province = models.CharField(max_length=200, null=True, verbose_name='استان')
    def sum_basket(self):
        t = 0
        for item in self.cartdetailmodel_set.all():
            t += item.final_price()
        return t
    def tax(self):
        return int(self.sum_basket() * 0.1)
    def total_price(self):
        x = self.sum_basket() + self.tax()
        return int(x)
    def detail_count(self):
        t = 0
        for item in self.cartdetailmodel_set.all():
            t += 1
        return t
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبدهای خرید"

class CartDetailModel(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='محصول')
    count = models.IntegerField()
    def final_price(self):
        return self.product.price * self.count
    def __str__(self):
        return f'{self.product.title} - {self.cart.user.username}'