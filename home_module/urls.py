from django.urls import path

from cart_module.views import add_to_cart, change_count
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('change-count/', change_count, name='change_count'),
]
