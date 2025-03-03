from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from cart_module.models import CartModel, CartDetailModel
from django.contrib import messages
import re
from sitesetting_module.models import SiteSettingModel


# Create your views here.

@method_decorator(decorator=login_required, name='dispatch')
class MainDashboard(View):
    def get(self, request: HttpRequest):
        user = request.user
        user_carts = CartModel.objects.filter(user_id=user.id, is_paid=True)
        settings = SiteSettingModel.objects.filter(is_active=True).first()
        return render(request, 'my-account.html', {
            'user': user,
            'carts': user_carts,
            'settings': settings,
        })

    def is_valid_phone_number(self, phone):
        phone = phone.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
        iranian_phone_pattern = re.compile(r"^(?:\+98|0)?9[0-9]{9}$")
        return iranian_phone_pattern.match(phone) is not None

    def is_valid_email(self, email):
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        return email_pattern.match(email) is not None

    def post(self, request: HttpRequest):
        user = request.user

        if 'user-info-form' in request.POST:
            first_name = request.POST['first-name']
            last_name = request.POST['last-name']
            province = request.POST['province']
            address = request.POST['address']
            phone = request.POST['phone']
            email = request.POST['email']
            if not self.is_valid_phone_number(phone):
                return render(request, 'my-account.html', {
                    'invalid_phone': True
                })
            if not self.is_valid_email(email):
                return render(request, 'my-account.html', {
                    'invalid_email': True
                })
            if len(str(email.strip())) > 6 and len(str(phone.strip())) > 10:
                user.first_name = first_name
                user.last_name = last_name
                user.province = province
                user.address = address
                user.phone = phone
                user.email = email
                user.save()
                messages.success(request, 'اطلاعات کاربر با موفقیت به‌روزرسانی شد.')
            elif len(str(phone.strip())) < 11:
                messages.error(request, 'شماره موبایل صحیح نیست')
            elif len(str(email.strip())) < 7:
                messages.error(request, 'ایمیل صحیح نیست')
            else:
                messages.error(request, 'ایمیل و شماره موبایل صحیح نیستند')
        elif 'password-change-form' in request.POST:
            old_pass = request.POST['old-password']
            new_pass = request.POST['new-password']
            re_new_pass = request.POST['re-new-password']

            if user.check_password(old_pass):
                if new_pass == re_new_pass:
                    user.set_password(new_pass)
                    user.save()
                    messages.success(request, 'رمز عبور با موفقیت تغییر یافت.')
                    return redirect('login')
                else:
                    messages.error(request, 'رمز عبور جدید و تکرار آن همخوانی ندارند.')
            else:
                messages.error(request, 'رمز عبور فعلی اشتباه است.')

        return redirect('main-dash')


@login_required
def detail_cart(request, id):
    details = CartDetailModel.objects.filter(cart_id=id)
    if len(details) > 0:
        return render(request, '', {
            'details': details,
        })
