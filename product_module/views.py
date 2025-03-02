from itertools import product
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string

from sitesetting_module.models import *
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from cart_module.models import CartModel
from .models import *
import json
from blog_module.models import CommentModel


# Create your views here.

class ProductList(ListView):
    template_name = 'product_list.html'
    model = ProductModel
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart = CartModel.objects.filter(user_id=user.id, is_paid=False).first()
        settings = SiteSettingModel.objects.filter(is_active=True).first()
        context['cart'] = cart
        context['settings'] = settings
        return context

# class ProductList(View):
#     def get(self, request):
#         products = ProductModel.objects.all()
#         return render(request, 'product_list.html', {
#             'products': products
#         })

# def product_list(request):
#     products = ProductModel.objects.all()
#     return render(request, 'product_list.html', {
#         'products': products
#     })

class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    model = ProductModel
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = self.object
        context['tags'] = ProductBrand.objects.filter(productmodel=product)
        product.visited += 1
        product.save()
        user = self.request.user
        if user.is_authenticated:
            cart = CartModel.objects.filter(user_id=user.id, is_paid=False).first()
        else:
            cart = None
        context['cart'] = cart
        context['comments'] = ProductCommentModel.objects.filter(product=product, is_publish=True)
        return context



# class ProductDetailView(View):
#     def get(self, request, slug):
#         product = ProductModel.objects.filter(slug=slug).first()
#         tags = ProductBrand.objects.filter(productmodel=product)
#         return render(request, 'product_detail.html', {
#             'product': product,
#             'tags': tags
#         })

# def product_detail(request, slug):
#     product = ProductModel.objects.filter(slug=slug).first()
#     tags = ProductBrand.objects.filter(productmodel=product)
#     return render(request, 'product_detail.html', {
#         'product': product,
#         'tags': tags
#     })


def category(request, slug):
    category = ProductCategory.objects.filter(slug=slug).first()
    products = ProductModel.objects.filter(category=category)
    user = request.user
    cart = CartModel.objects.filter(user_id=user.id, is_paid=False).first()
    return render(request, 'product_list.html', {
        'products': products,
        'cart': cart
    })


def tags(request, slug):
    tag = ProductBrand.objects.filter(url=slug).first()
    products = ProductModel.objects.filter(brand=tag)
    user = request.user
    cart = CartModel.objects.filter(user_id=user.id, is_paid=False).first()
    return render(request, 'product_list.html', {
        'products': products,
        'cart': cart
    })


def render_partial_sidebar(request):
    brands = ProductCategory.objects.all()
    user = request.user
    cart = CartModel.objects.filter(user_id=user.id, is_paid=False).first()
    return render(request, 'sidebar.html', {
        'brands': brands,
        'cart': cart
    })


def header_component(request):
    settings = SiteSettingModel.objects.filter(is_active=True).first()
    user = request.user
    cart = CartModel.objects.filter(user_id=user.id, is_paid=False).first()
    return render(request, 'header2_component.html', {
        'settings': settings,
        'cart': cart
    })


@login_required
def send_product_comment(request, slug):
    tag = ProductBrand.objects.filter(url=slug).first()
    text = request.GET.get("text")
    product_id = int(request.GET.get("product_id"))
    new_comment = ProductCommentModel.objects.create(user=request.user, text=text, product_id=product_id,
                                                     is_publish=True)
    comments = ProductCommentModel.objects.filter(product_id=product_id, is_publish=True)
    products = ProductModel.objects.filter(brand=tag)
    return render(request, 'product-comment-box.html', {
        'comments': comments,
        'count_comment': len(comments),
        'products': products,
    })


@login_required
def submit_comment_and_rating(request, slug):
    user = request.user
    product_id = int(request.POST.get('product_id'))
    text = request.POST.get('text')
    rate = request.POST.get('rate')

    if not text.strip():
        return JsonResponse({"status": "error", "message": "متن کامنت نمی‌تواند خالی باشد"})
    if not rate:
        return JsonResponse({"status": "error", "message": "رتبه‌بندی نمی‌تواند خالی باشد"})

    rate = int(rate)

    new_comment = ProductCommentModel.objects.create(user=user, text=text, product_id=product_id, rating=rate)

    comments = ProductCommentModel.objects.filter(product_id=product_id, is_publish=True)
    return JsonResponse({"status": "success"})
