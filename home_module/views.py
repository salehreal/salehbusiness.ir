from django.conf import settings
from django.shortcuts import render
from sitesetting_module.models import *
from django.views import View
from django.views.generic import TemplateView
from sitesetting_module.models import SiteSettingModel
from product_module.models import *
from cart_module.models import CartModel


# Create your views here.


class HomeView(View):
    def get(self, request):
        sliders = SliderModel.objects.filter(is_active=True)
        category = ProductCategory.objects.filter(is_active=True)
        user = request.user
        cart = CartModel.objects.filter(user_id=user.id, is_paid=False).first()
        product = ProductModel.objects.filter(is_active=True).first()
        return render(request, 'home.html', {
            'sliders': sliders,
            'category': category,
            'cart': cart,
            'product': product,
        })
    # def get(self, request):
    #     return render(request, 'home.html', {
    #
    #     })
# def home(request):
#     return render(request, 'home.html', {
#
#     })





def header_component(request):
    settings = SiteSettingModel.objects.filter(is_active=True).first()
    return render(request, 'header1_component.html', {
        'settings': settings,
    })


def footer_component(request):
    settings = SiteSettingModel.objects.filter(is_active=True).first()
    return render(request, 'footer_component.html', {
        'settings': settings,
    })