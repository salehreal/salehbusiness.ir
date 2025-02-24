from django.contrib import admin
from .models import BlogModel, CommentModel
from jalali_date.admin import ModelAdminJalaliMixin
# Register your models here.

class BlogAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_editable = ['is_active']
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        return super(BlogAdmin, self).save_model(request, obj, form, change)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', 'blog', 'is_publish']
    list_editable = ['is_publish']

admin.site.register(BlogModel, BlogAdmin)
admin.site.register(CommentModel, CommentAdmin)