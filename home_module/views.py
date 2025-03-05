from django.conf import settings
from django.shortcuts import render, redirect
from django.template.defaulttags import comment
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
        new_products = ProductModel.objects.filter(is_active=True).order_by("-created_at")[:8]
        visited_product = ProductModel.objects.filter(is_active=True).order_by("-visited")[:8]
        category = ProductCategory.objects.filter(is_active=True)
        user = request.user
        cart = CartModel.objects.filter(user_id=user.id, is_paid=False).first()
        product = ProductModel.objects.filter(is_active=True).first()
        comments = ProductCommentModel.objects.filter(product=product, is_publish=True).order_by("-rating")[:4]
        return render(request, 'home.html', {
            'sliders': sliders,
            'category': category,
            'cart': cart,
            'product': product,
            'new_products': new_products,
            'visited_product': visited_product,
            'comments': comments,
        })

    def post(self, request):
        search = request.POST['prod-search']
        products = ProductModel.objects.filter(title__icontains=search)
        return render(request, 'product_list.html', {
            'products': products
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
    user = request.user
    cart = CartModel.objects.filter(user_id=user.id, is_paid=False).first()
    return render(request, 'header1_component.html', {
        'settings': settings,
        'cart': cart,
    })


def footer_component(request):
    settings = SiteSettingModel.objects.filter(is_active=True).first()
    return render(request, 'footer_component.html', {
        'settings': settings,
    })