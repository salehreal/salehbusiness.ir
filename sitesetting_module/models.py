from django.db import models

# Create your models here.

class SiteSettingModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام فروشگاه")
    logo = models.ImageField(upload_to="logo", verbose_name="لوگو")
    email = models.EmailField(max_length=100, verbose_name="ایمیل")
    phone = models.CharField(max_length=20, verbose_name="تلفن")
    fax = models.CharField(max_length=50, null=True, blank=True, verbose_name="فکس (اختیاری)")
    address = models.TextField(null=True, blank=True, verbose_name="آدرس (اختیاری)")
    working_start_day = models.CharField(max_length=50, null=True, blank=True, verbose_name="اولین روز کاری (اختیاری)")
    working_end_day = models.CharField(max_length=50, null=True, blank=True, verbose_name="آخرین روز کاری (اختیاری)")
    working_start_hour = models.CharField(max_length=50, null=True, blank=True, verbose_name="ساعت شروع کار (اختیاری)")
    working_end_hour = models.CharField(max_length=50, null=True, blank=True, verbose_name="ساعت پایان کار (اختیاری)")
    social_instagram = models.CharField(max_length=150, null=True, blank=True, verbose_name="اینستاگرام (اختیاری)")
    social_twitter = models.CharField(max_length=150, null=True, blank=True, verbose_name="توئیتر (اختیاری)")
    social_telegram = models.CharField(max_length=150, null=True, blank=True, verbose_name="تلگرام (اختیاری)")
    social_youtube = models.CharField(max_length=150, null=True, blank=True, verbose_name="یوتیوب (اختیاری)")
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تنظیم"
        verbose_name_plural = "تنظیمات"

class SliderModel(models.Model):
    products = models.ManyToManyField('product_module.ProductModel', verbose_name="محصولات")
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")

    def __str__(self):
        return ', '.join([product.title for product in self.products.all()])

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدر ها'


class AboutUsModel(models.Model):
    image1 = models.ImageField(upload_to="aboutus", verbose_name="تصویر1")
    title1 = models.CharField(max_length=100, verbose_name="عنوان1")
    text1 = models.TextField(verbose_name="متن1")
    image2 = models.ImageField(upload_to="aboutus", null=True, blank=True, verbose_name="تصویر2 (اختیاری)")
    title2 = models.CharField(max_length=100, null=True, blank=True, verbose_name="عنوان2 (اختیاری)")
    text2 = models.TextField(null=True, blank=True, verbose_name="متن2 (اختیاری)")
    image3 = models.ImageField(upload_to="aboutus", null=True, blank=True, verbose_name="تصویر3 (اختیاری)")
    title3 = models.CharField(max_length=100, null=True, blank=True, verbose_name="عنوان3 (اختیاری)")
    text3 = models.TextField(null=True, blank=True, verbose_name="متن3 (اختیاری)")
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")
    def __str__(self):
        return self.title1
    class Meta:
        verbose_name = 'درباره ما'
        verbose_name_plural = 'درباره ما'


class QuestionsModel(models.Model):
    question1 = models.CharField(max_length=1000, verbose_name='سوال۱')
    answer1 = models.TextField(verbose_name='پاسخ۱')
    question2 = models.CharField(max_length=1000, verbose_name='سوال۲ (اختیاری)', null=True, blank=True)
    answer2 = models.TextField(verbose_name='پاسخ۲ (اختیاری)', null=True, blank=True)
    question3 = models.CharField(max_length=1000, verbose_name='سوال۳ (اختیاری)', null=True, blank=True)
    answer3 = models.TextField(verbose_name='پاسخ۳ (اختیاری)', null=True, blank=True)
    question4 = models.CharField(max_length=1000, verbose_name='سوال۴ (اختیاری)', null=True, blank=True)
    answer4 = models.TextField(verbose_name='پاسخ۴ (اختیاری)', null=True, blank=True)
    question5 = models.CharField(max_length=1000, verbose_name='سوال۵ (اختیاری)', null=True, blank=True)
    answer5 = models.TextField(verbose_name='پاسخ۵ (اختیاری)', null=True, blank=True)
    question6 = models.CharField(max_length=1000, verbose_name='سوال۶ (اختیاری)', null=True, blank=True)
    answer6 = models.TextField(verbose_name='پاسخ۶ (اختیاری)', null=True, blank=True)
    question7 = models.CharField(max_length=1000, verbose_name='سوال۷ (اختیاری)', null=True, blank=True)
    answer7 = models.TextField(verbose_name='پاسخ۷ (اختیاری)', null=True, blank=True)
    question8 = models.CharField(max_length=1000, verbose_name='سوال۸ (اختیاری)', null=True, blank=True)
    answer8 = models.TextField(verbose_name='پاسخ۸ (اختیاری)', null=True, blank=True)
    question9 = models.CharField(max_length=1000, verbose_name='سوال۹ (اختیاری)', null=True, blank=True)
    answer9 = models.TextField(verbose_name='پاسخ۹ (اختیاری)', null=True, blank=True)
    question10 = models.CharField(max_length=1000, verbose_name='سوال۱۰ (اختیاری)', null=True, blank=True)
    answer10 = models.TextField(verbose_name='پاسخ۱۰ (اختیاری)', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")
    def __str__(self):
        return self.question1
    class Meta:
        verbose_name = 'سوال متداول'
        verbose_name_plural = 'سوالات متداول'
