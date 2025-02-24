from django.contrib import admin
from .models import ProductModel, ProductCategory, Inform, ProductBrand, ProductCommentModel

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'is_active', 'get_datetime_fa']
    list_editable = ['price', 'is_active']
    list_filter = ['price', 'created_at', 'cylinder_count', 'seat_count']
    ordering = ['price']
    prepopulated_fields = {
        'slug': ('title',),
    }

class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'product', 'is_publish')
    list_editable = ['is_publish']
    list_filter = ('is_publish', 'create')
    search_fields = ('user__username', 'text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_publish=True)
    approve_comments.short_description = 'تأیید کامنت‌های انتخابی'


admin.site.register(ProductModel, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(Inform)
admin.site.register(ProductBrand)
admin.site.register(ProductCommentModel, ProductCommentAdmin)
