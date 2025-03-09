from django.contrib import admin
from .models import ContactUsModel
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone']

admin.site.register(ContactUsModel, ContactAdmin)
