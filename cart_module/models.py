from django.db import models
from user_module.models import User
from product_module.models import ProductModel
from sitesetting_module.models import SiteSettingModel
from django.utils.timezone import now
from sitesetting_module.models import DiscountCodeModel
# Create your models here.

from django.db import models
from django.utils import timezone

from django.db import models
from django.utils import timezone


class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده / نشده')
    payment_date = models.DateTimeField(null=True, verbose_name='تاریخ پرداخت')
    process = models.BooleanField(default=False, verbose_name='درحال پردازش')
    delivery = models.BooleanField(default=False, verbose_name='تحویل شده')

    def save(self, *args, **kwargs):
        if self.is_paid and self.payment_date is None:
            self.payment_date = timezone.now()
        super(CartModel, self).save(*args, **kwargs)

    def sum_basket(self):
        t = 0
        for item in self.cartdetailmodel_set.all():
            final_price = item.final_price()
            t += final_price if final_price is not None else 0
        return t

    def total_price(self, discount_code=None):
        setting = SiteSettingModel.objects.first()
        sum_basket = self.sum_basket()
        send = setting.send_cost if setting and setting.send_cost else 0

        # بررسی اعتبار کد تخفیف
        if discount_code:
            try:
                discount = DiscountCodeModel.objects.get(
                    code=discount_code, is_active=True, valid_from__lte=now(), valid_until__gte=now()
                )
                discount_amount = float(discount.discount_amount)  # مقدار تخفیف به صورت درصد
                sum_basket -= sum_basket * discount_amount
            except DiscountCodeModel.DoesNotExist:
                # اگر کد تخفیف معتبر نباشد
                pass

        # قیمت نهایی (سبد خرید + هزینه ارسال)
        return int(sum_basket + send)

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
        if self.product.discount is not None:
            discount = float(self.product.discount)
        else:
            discount = 0
        product_price = self.product.price * (1 - discount) if self.product.price is not None else 0
        count = self.count if self.count is not None else 0
        return int(product_price * count)

    def __str__(self):
        return f'{self.product.title} - {self.cart.user.username}'

    class Meta:
        verbose_name = "جزئیات سبد خرید"
        verbose_name_plural = "جزئیات سبدهای خرید"

class BuyerModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    cart = models.ForeignKey(CartModel, verbose_name='سبد خرید', null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=100, verbose_name='نام', blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی', blank=True, null=True)
    province = models.CharField(max_length=100, verbose_name="استان", blank=True, null=True)
    address = models.TextField(verbose_name='آدرس', blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name='شماره تلفن', blank=True, null=True)
    describe = models.TextField(verbose_name='توضیحات', blank=True, null=True)
    payment_date = models.DateTimeField(verbose_name='تاریخ پرداخت', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.cart and self.payment_date is None:
            self.payment_date = timezone.now()
            self.cart.payment_date = self.payment_date
            self.cart.is_paid = True
            self.cart.save()
        super(BuyerModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.payment_date

    class Meta:
        verbose_name = "پردختی"
        verbose_name_plural = "پرداختی ها"

