from django.urls import path
from .views import *

urlpatterns = [
    path('basket/', Basket.as_view(), name='basket'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('change-count/', change_count),
    path('delete-detail/', delete_detail),
    path('delete-cart/', delete_cart)
]
