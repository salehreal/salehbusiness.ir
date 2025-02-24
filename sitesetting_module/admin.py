from django.contrib import admin
from .models import SiteSettingModel, SliderModel, AboutUsModel
# Register your models here.
admin.site.register(SiteSettingModel)
admin.site.register(SliderModel)
admin.site.register(AboutUsModel)