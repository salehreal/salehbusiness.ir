from django.urls import path
from .views import *
from . import views
from azbankgateways.urls import az_bank_gateways_urls
from django.contrib import admin

admin.autodiscover()
urlpatterns = [
    path("bankgateways/", az_bank_gateways_urls(), name='gateway'),
    path('basket/', Basket.as_view(), name='basket'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('change-count/', change_count),
    path('delete-detail/', delete_detail),
    path('delete-cart/', delete_cart),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('checkout/validate-coupon/', views.validate_coupon, name='validate-coupon'),
]
