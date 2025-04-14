from itertools import product
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, QueryDict
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
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
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()

        # دریافت پارامتر دسته‌بندی از URL
        category_slug = self.request.GET.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)  # فیلتر بر اساس دسته‌بندی

        # تنظیم مرتب‌سازی بر اساس sort_by
        sort_by = self.request.GET.get('sort_by', '-price')
        if sort_by == 'price':
            queryset = queryset.order_by('price')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'sale':
            queryset = queryset.order_by('-added_to_cart_count')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort_by == 'visit':
            queryset = queryset.order_by('-visited')
        elif sort_by == 'discount':
            queryset = queryset.order_by('-discount')
        else:
            queryset = queryset.order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart = CartModel.objects.filter(user_id=user.id, is_paid=False).first()
        settings = SiteSettingModel.objects.filter(is_active=True).first()
        total_products = ProductModel.total_products()
        context['total_products'] = total_products
        context['cart'] = cart
        context['settings'] = settings

        # حفظ پارامترهای sort_by در لینک‌های صفحه‌بندی
        querydict = QueryDict(mutable=True)
        querydict['sort_by'] = self.request.GET.get('sort_by', '-price')
        context['query_string'] = querydict.urlencode()
        return context


class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    model = ProductModel
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = self.object
        context['tags'] = product.brand.all()
        related_products = ProductModel.objects.filter(brand__in=product.brand.all()).exclude(id=product.id).distinct()
        context['related_products'] = related_products
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


@csrf_exempt
def filter_products(request):
    if request.method == "POST":
        data = json.loads(request.body)
        categories = data.get('categories', [])
        page_number = data.get('page', 1)  # صفحه‌ی موردنظر
        products = ProductModel.objects.filter(category__slug__in=categories).distinct()

        # صفحه‌بندی
        paginator = Paginator(products, 12)  # هر صفحه شامل 12 محصول
        page_obj = paginator.get_page(page_number)

        product_list = [
            {
                "id": p.id,
                "title": p.title,
                "slug": p.slug,
                "image": p.mainimage.url if p.mainimage else None,
                "price": p.price,
            } for p in page_obj
        ]

        # بازگرداندن اطلاعات صفحه‌بندی و محصولات
        return JsonResponse({
            "products": product_list,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "total_pages": paginator.num_pages,  # تعداد کل صفحات
            "current_page": page_obj.number,  # شماره صفحه فعلی
        })

    return JsonResponse({"error": "Invalid request method"}, status=400)


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
