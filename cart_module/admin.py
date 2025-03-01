from django.contrib import admin
from .models import CartModel, CartDetailModel
# Register your models here.

admin.site.register(CartModel)
admin.site.register(CartDetailModel)