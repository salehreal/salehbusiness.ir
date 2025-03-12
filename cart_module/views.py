import re
from datetime import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404, HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views import View
from product_module.models import ProductModel
from sitesetting_module.models import SiteSettingModel, DiscountCodeModel, DiscountCodeUsage
from .models import CartModel, CartDetailModel, BuyerModel
import logging
from user_module.models import User
from django.urls import reverse
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from azbankgateways.exceptions import AZBankGatewaysException


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

    def is_valid_persian_name(self, name):
        persian_name_pattern = re.compile(r'^[\u0600-\u06FF\s]+$')
        return persian_name_pattern.match(name) is not None

    def post(self, request: HttpRequest):
        user = request.user
        user_carts = CartModel.objects.filter(user_id=user.id, is_paid=True)
        settings = SiteSettingModel.objects.filter(is_active=True).first()

        if 'user-cart-info-form' in request.POST:
            first_name = request.POST['first-name']
            last_name = request.POST['last-name']
            province = request.POST['province']
            address = request.POST['address']
            phone = request.POST['phone']
            describe = request.POST['describe']

            if len(address) < 10:
                messages.error(request, 'آدرس حداقل باید شامل ۱۰ کاراکتر باشد.')
                return render(request, 'content-checkout.html', {
                    'user': user,
                    'carts': user_carts,
                    'settings': settings,
                })

            if not self.is_valid_persian_name(first_name):
                messages.error(request, 'نام باید فقط شامل حروف فارسی باشد.')
                return render(request, 'content-checkout.html', {
                    'user': user,
                    'carts': user_carts,
                    'settings': settings,
                })

            if not self.is_valid_persian_name(last_name):
                messages.error(request, 'نام خانوادگی باید فقط شامل حروف فارسی باشد.')
                return render(request, 'content-checkout.html', {
                    'user': user,
                    'carts': user_carts,
                    'settings': settings,
                })

            # ادامه عملیات ذخیره اطلاعات
            cart = CartModel.objects.filter(user_id=user.id, is_paid=False).first()
            if cart:
                BuyerModel.objects.create(
                    user=user,
                    cart=cart,
                    payment_date=timezone.now(),
                    first_name=first_name,
                    last_name=last_name,
                    province=province,
                    address=address,
                    phone=phone,
                    describe=describe
                )
                cart.is_paid = True
                cart.payment_date = timezone.now()
                cart.save()

            messages.success(request, 'پرداخت با موفقیت ثبت شد.')
            return redirect('gateway')

        # مسیر پیش‌فرض برای بازگشت پاسخ
        return render(request, 'checkout.html', {
            'cart': None,
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


def go_to_gateway_view(request):
    user = request.user
    user_cart = CartModel.objects.filter(user=user, is_paid=False).first()
    # خواندن مبلغ از هر جایی که مد نظر است
    amount = (user_cart.total_price()) * 10
    # تنظیم شماره موبایلa کاربر از هر جایی که مد نظر است
    # user_mobile_number = user.phone  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = (
            factory.auto_create()
        )  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse("callback-gateway"))
        # bank.set_mobile_number(user_mobile_number)  # اختیاری

        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید.
        bank_record = bank.ready()

        # هدایت کاربر به درگاه بانک
        context = bank.get_gateway()
        return render(request, "redirect_to_bank.html", context=context)
    except AZBankGatewaysException as e:
        logging.critical(e)
        return render(request, "redirect_to_bank.html")


def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        return HttpResponse("پرداخت با موفقیت انجام شد.")

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse(
        "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت."
    )
