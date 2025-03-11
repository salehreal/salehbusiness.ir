from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('basket/', Basket.as_view(), name='basket'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('change-count/', change_count),
    path('delete-detail/', delete_detail),
    path('delete-cart/', delete_cart),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('checkout/validate-coupon/', views.validate_coupon, name='validate-coupon'),
]
