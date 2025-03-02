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
            final_price = item.final_price()
            t += final_price if final_price is not None else 0
        return t

    def tax(self):
        sum_basket = self.sum_basket()
        return int(sum_basket * 0.1) if sum_basket is not None else 0

    def total_price(self):
        sum_basket = self.sum_basket()
        tax = self.tax()
        return int(sum_basket + tax) if sum_basket is not None and tax is not None else 0

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
        product_price = self.product.price if self.product.price is not None else 0
        count = self.count if self.count is not None else 0
        return product_price * count

    def __str__(self):
        return f'{self.product.title} - {self.cart.user.username}'

