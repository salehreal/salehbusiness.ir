from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.views import View
from product_module.models import ProductModel
from sitesetting_module.models import SiteSettingModel, DiscountCodeModel, DiscountCodeUsage
from .forms import DiscountCodeForm
from .models import CartModel, CartDetailModel


# Create your views here.

class Basket(View):
    def get(self, request):
        user = request.user
        cart = CartModel.objects.filter(user_id=user.id, is_paid=False).first()
        return render(request, 'basket.html', {
            'cart': cart,
        })


class Checkout(View):
    def get(self, request):
        user = request.user
        cart = CartModel.objects.filter(user_id=user.id, is_paid=False).first()
        settings = SiteSettingModel.objects.filter(is_active=True).first()
        return render(request, 'checkout.html', {
            'cart': cart,
            'settings': settings,
            'user': user,
        })


def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        return JsonResponse({'status': "not_login"})
    try:
        product_id = request.GET.get("product_id")
        count = request.GET.get("count")
        if product_id is None or count is None:
            raise ValueError("Missing product_id or count")
        product_id = int(product_id)
        count = int(count)
    except Exception as e:
        return JsonResponse({'status': "error"})
    if count < 1:
        return JsonResponse({'status': "amount"})
    product = ProductModel.objects.filter(id=product_id).first()
    if product is None:
        return JsonResponse({'status': "error"})

    cart, created = CartModel.objects.get_or_create(user_id=user.id, is_paid=False)

    detail = CartDetailModel.objects.filter(cart_id=cart.id, product_id=product_id).first()
    if detail is not None:
        detail.count += count
        if detail.count > product.count:
            return JsonResponse({'status': "amount"})
        detail.save()
    else:
        if count > product.count:
            return JsonResponse({'status': "amount"})
        detail = CartDetailModel(cart_id=cart.id, product_id=product_id, count=count)
        detail.save()

    product.added_to_cart_count += count
    product.save()

    return JsonResponse({'status': "ok"})


@login_required
def change_count(request):
    try:
        detail_id = int(request.GET.get("detail_id"))
        state = request.GET.get("state")
    except:
        return JsonResponse({'status': "error"})
    detail = CartDetailModel.objects.filter(id=detail_id).first()
    product = ProductModel.objects.filter(id=detail.product_id).first()
    if detail is not None:
        if state == 'pos':
            detail.count += 1
            if detail.count > product.count:
                return JsonResponse({'status': "amount"})
            else:
                detail.save()
        elif state == 'neg':
            if detail.count == 1:
                detail.delete()
            else:
                detail.count += -1
                detail.save()
    else:
        return JsonResponse({'status': "error"})
    cart = CartModel.objects.filter(user_id=request.user.id).first()
    return render(request, 'content-basket.html', {
        'cart': cart
    })


@login_required
def delete_detail(request):
    try:
        detail_id = int(request.GET.get("detail_id"))
    except:
        return JsonResponse({'status': "error"})
    detail = CartDetailModel.objects.filter(id=detail_id).first()
    detail.delete()
    cart = CartModel.objects.filter(user_id=request.user.id).first()
    return render(request, 'content-basket.html', {
        'cart': cart
    })


@login_required
def delete_cart(request):
    try:
        cart_id = int(request.GET.get("cart_id"))
    except:
        return JsonResponse({'status': "error"})
    cart = CartModel.objects.filter(user_id=request.user.id).first()
    cart.delete()
    cart = CartModel.objects.filter(user_id=request.user.id).first()
    return render(request, 'content-basket.html', {
        'cart': cart
    })


def validate_coupon(request):
    code = request.GET.get("code")
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({"valid": False, "message": "ابتدا وارد حساب کاربری خود شوید."})

    try:
        discount = DiscountCodeModel.objects.get(
            code=code, is_active=True, valid_from__lte=now(), valid_until__gte=now()
        )

        # بررسی استفاده قبلی از کد
        if DiscountCodeUsage.objects.filter(user=user, discount_code=discount).exists():
            return JsonResponse({"valid": False, "message": "این کد تخفیف قبلاً استفاده شده است."})

        # ذخیره استفاده از کد تخفیف
        DiscountCodeUsage.objects.create(user=user, discount_code=discount)

        return JsonResponse({"valid": True, "discount": discount.discount_amount})
    except DiscountCodeModel.DoesNotExist:
        return JsonResponse({"valid": False, "message": "کد تخفیف نامعتبر است."})
