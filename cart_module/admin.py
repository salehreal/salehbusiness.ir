from django.contrib import admin
from .models import CartModel, CartDetailModel, BuyerModel
# Register your models here.

admin.site.register(CartModel)
admin.site.register(CartDetailModel)
admin.site.register(BuyerModel)