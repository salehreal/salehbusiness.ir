from django.contrib import admin
from .models import SliderModel
from product_module.models import ProductModel


@admin.register(SliderModel)
class SliderModelAdmin(admin.ModelAdmin):
    list_display = ['get_product_titles', 'is_active']
    list_filter = ['is_active']
    search_fields = ['products__title']
    list_editable = ['is_active']

    def get_product_titles(self, obj):
        return ', '.join([product.title for product in obj.products.all()])
    get_product_titles.short_description = 'محصولات'
