from tkinter.constants import CASCADE
from django.db import models
import jdatetime
from user_module.models import User


# Create your models here.


class ProductCategory(models.Model):
    image = models.ImageField(upload_to="category", verbose_name="تصویر")
    title = models.CharField(max_length=300, verbose_name="عنوان")
    slug = models.SlugField(max_length=200, null=True, db_index=True, allow_unicode=True, unique=True,
                            verbose_name='آدرس در مرورگر', blank=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")

    def save(self, *args, **kwargs):
        self.slug = self.title.replace(' ', '-')
        return super(ProductCategory, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductBrand(models.Model):
    title = models.CharField(max_length=300, verbose_name="عنوان")
    url = models.CharField(max_length=200, verbose_name='آدرس در مرورگر')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'


class Inform(models.Model):
    id_for = models.IntegerField(verbose_name='کد شناسایی')
    year = models.CharField(max_length=150, verbose_name='سال تولید')
    made_in = models.CharField(max_length=200, verbose_name='کشور سازنده')

    def __str__(self):
        return str(self.id_for)

    class Meta:
        verbose_name = 'اطلاعات محصول'
        verbose_name_plural = 'اطلاعات محصولات'


class ProductModel(models.Model):
    class ChoiceCylinder:
        STATUS_CHOICES = (
            ('0', '0 Cylinder'), ('3', '3 Cylinders'), ('4', '4 Cylinders'), ('6', '6 Cylinders'), ('8', '8 Cylinders'),
            ('10', '10 Cylinders'), ('12', '12 Cylinders'), ('16', '16 Cylinders'))

    class ChoiceSeat:
        STATUS_CHOICES = (('4', '4 Seats'), ('5', '5 Seats'), ('7', '7 Seats'))

    class ChoiceDiscount:
        STATUS_CHOICES = (
            ('0.05', '5%'), ('0.1', '10%'), ('0.15', '15%'), ('0.2', '20%'), ('0.25', '25%'), ('0.3', '30%'),
            ('0.35', '35%'),
            ('0.4', '40%'), ('0.45', '45%'), ('0.5', '50%'), ('0.55', '55%'), ('0.6', '60%'), ('0.65', '65%'),
            ('0.7', '70%'),
            ('0.75', '75%'), ('0.8', '80%'), ('0.85', '85%'), ('0.9', '90%'), ('0.95', '95%'),)

    mainimage = models.ImageField(upload_to='products', verbose_name='تصویر اصلی محصول', null=True)
    image1 = models.ImageField(upload_to='products', verbose_name='تصویر محصول', null=True, blank=True)
    image2 = models.ImageField(upload_to='products', verbose_name='تصویر محصول', null=True, blank=True)
    image3 = models.ImageField(upload_to='products', verbose_name='تصویر محصول', null=True, blank=True)
    title = models.CharField(max_length=300, verbose_name='عنوان')
    price = models.IntegerField(verbose_name='قیمت')
    descript = models.TextField(verbose_name='توضیحات')
    created_at = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    count = models.IntegerField(null=True, verbose_name='تعداد')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE, verbose_name='دسته بندی', null=True)
    inform = models.OneToOneField(Inform, on_delete=models.CASCADE, verbose_name='اطلاعات محصول', null=True)
    brand = models.ManyToManyField(ProductBrand, verbose_name='تگ')
    visited = models.IntegerField(default=0, verbose_name='بازدید')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    cylinder_count = models.CharField(max_length=20, null=True, verbose_name='تعداد سیلندر',
                                      choices=ChoiceCylinder.STATUS_CHOICES)
    seat_count = models.CharField(max_length=20, null=True, verbose_name='تعداد صندلی',
                                  choices=ChoiceSeat.STATUS_CHOICES)
    discount = models.CharField(max_length=20, null=True, blank=True, verbose_name='تخفیف',
                                choices=ChoiceDiscount.STATUS_CHOICES)
    slug = models.SlugField(max_length=200, null=True, db_index=True, allow_unicode=True, unique=True,
                            verbose_name='آدرس در مرورگر', blank=True)

    def save(self, *args, **kwargs):
        self.slug = self.title.replace(' ', '-')
        return super(ProductModel, self).save(*args, **kwargs)

    def get_datetime_fa(self):
        date_fa = jdatetime.GregorianToJalali(self.created_at.year, self.created_at.month, self.created_at.day)
        final_date = date_fa.getJalaliList()
        return f'{final_date[0]} - {final_date[1]} - {final_date[2]}'

    def rating_avg(self):
        total = 0
        c = 0
        for comment in self.productcommentmodel_set.all():
            if comment.rating:
                total += comment.rating
                c += 1
        if c > 0:
            avg = round(total / c)
        else:
            avg = 0
        return avg

    def final_price(self):
        if self.price and self.discount:
            discount_value = float(self.discount)
            return int(self.price * (1 - discount_value))
        else:
            return int(self.price)

    def get_discount_display(self):
        for choice in self.ChoiceDiscount.STATUS_CHOICES:
            if self.discount == choice[0]:
                return choice[1]
        return None

    def comment_count(self):
        return self.productcommentmodel_set.count()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class ProductCommentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    create = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name='متن کامنت')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='محصول', db_index=True)
    is_publish = models.BooleanField(default=False, verbose_name='منتشر')
    rating = models.IntegerField(null=True, blank=True, verbose_name='رتبه')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'کامنت محصول'
        verbose_name_plural = 'کامنت‌های محصول'
