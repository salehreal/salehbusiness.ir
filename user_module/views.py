import random
from django.contrib.auth import login, logout
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views import View

from sitesetting_module.models import SiteSettingModel
from .models import User
from utils.utils import create_random_code
from .forms import ActiveForm
import re


# Create your views here.

class Register(View):
    def get(self, request):
        settings = SiteSettingModel.objects.filter(is_active=True).first()
        return render(request, 'register-page.html', {
            'settings': settings
        })

    def generate_unique_username(self):
        while True:
            username = ''.join(random.choices('0123456789', k=8))
            if not User.objects.filter(username=username).exists():
                return username

    def is_valid_persian_name(self, name):
        persian_name_pattern = re.compile(r'^[\u0600-\u06FF\s]+$')
        return persian_name_pattern.match(name) is not None

    def is_valid_phone_number(self, phone):
        phone = phone.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
        iranian_phone_pattern = re.compile(r"^(?:\+98|0)?9[0-9]{9}$")
        return iranian_phone_pattern.match(phone) is not None

    # def is_valid_email(self, email):
    #     email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    #     return email_pattern.match(email) is not None

    def post(self, request: HttpRequest):
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        # email = request.POST.get('email', '')
        phone = request.POST.get('phone', '').translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
        password = request.POST.get('password', '').translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))

        error = False
        if not self.is_valid_persian_name(first_name):
            return render(request, 'register-page.html', {'invalid_first_name': True})

        if not self.is_valid_persian_name(last_name):
            return render(request, 'register-page.html', {'invalid_last_name': True})

        if not self.is_valid_phone_number(phone):
            return render(request, 'register-page.html', {
                'invalid_phone': True
            })

        # if not self.is_valid_email(email):
        #     return render(request, 'register-page.html', {
        #         'invalid_email': True
        #     })

        user = User.objects.filter(phone=phone).first()
        if user is not None:
            return render(request, 'register-page.html', {
                'exist': True
            })
        else:
            username = self.generate_unique_username()
            if len(phone.strip()) > 10 and len(password.strip()) > 5:
                new_user = User(first_name=first_name, last_name=last_name, username=username, phone=phone,
                                active_code=create_random_code(6),
                                token=get_random_string(100), is_active=False)
                new_user.set_password(raw_password=password)
                new_user.save()
                request.session['user_token'] = new_user.token
                request.session.set_expiry(190)
                return redirect('active-user')
            else:
                error = True

        return render(request, 'register-page.html', {
            'error': error
        })


class Login(View):
    def get(self, request):
        settings = SiteSettingModel.objects.filter(is_active=True).first()
        return render(request, 'login-page.html', {
            'settings': settings,
        })

    def post(self, request: HttpRequest):
        phone = request.POST.get('phone', '').translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
        password = request.POST.get('password', '').translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))

        user = User.objects.filter(phone=phone).first()
        if user is not None:
            if user.check_password(password):
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    new_user = User.objects.filter(phone=user.phone).first()
                    new_user.save()
                    request.session['user_token'] = new_user.token
                    request.session.set_expiry(190)
                    return redirect('active-user')
                    # send_sms(new_user.phone, new_user.active_code)
            else:
                return render(request, 'login-page.html', {
                    'error': True
                })
        else:
            return render(request, 'login-page.html', {
                'error': True
            })


class ActiveUserView(View):
    def get(self, request: HttpRequest):
        try:
            token = request.session['user_token']
        except:
            token = None
        user = User.objects.filter(token=token).first()
        if user is not None:
            form = ActiveForm()
            return render(request, 'active_user.html', {
                'form_active': form
            })
        else:
            return render(request, '404.html', {

            })

    def post(self, request):
        token = request.session.get('user_token')
        user = User.objects.filter(token=token).first()
        if user is not None:
            form = ActiveForm(request.POST)
            if form.is_valid():
                num1 = form.cleaned_data.get('num1')
                num2 = form.cleaned_data.get('num2')
                num3 = form.cleaned_data.get('num3')
                num4 = form.cleaned_data.get('num4')
                num5 = form.cleaned_data.get('num5')
                num6 = form.cleaned_data.get('num6')
                code_insert = f'{num1}{num2}{num3}{num4}{num5}{num6}'
                if code_insert == user.active_code:
                    user.is_active = True
                    user.token = get_random_string(100)
                    user.active_code = create_random_code(6)
                    user.save()
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'active_user.html', {
                        'form_active': form,
                        'error': True
                    })
            else:
                return render(request, 'active_user.html', {
                    'form_active': form,
                    'error': True
                })
        else:
            return render(request, '404.html', {

            })


class ForgetPassword(View):
    def get(self, request):
        return render(request, 'forget-password.html', {

        })

    def post(self, request: HttpRequest):
        phone = request.POST.get('phone', '').translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
        user = User.objects.filter(phone=phone).first()
        if user is not None:
            user.active_code = create_random_code(6)
            user.token = get_random_string(100)
            user.save()
            # send_sms(new_user.phone, new_user.active_code)
            request.session['forget-confirm'] = user.token
            return redirect('confirm-password')
        else:
            return render(request, 'forget-password.html', {
                'existError': True
            })


class ConfirmPasswordView(View):
    def get(self, request):
        try:
            cookie = request.session['forget-confirm']
        except:
            cookie = None
        if cookie:
            form = ActiveForm()
            return render(request, 'active_user.html', {
                'form_active': form
            })
        else:
            return render(request, '404.html', {

            })

    def post(self, request):
        try:
            cookie = request.session['forget-confirm']
        except:
            cookie = None
        user = User.objects.filter(token=cookie).first()
        if user is not None:
            form = ActiveForm(request.POST)
            if form.is_valid():
                num1 = form.cleaned_data.get('num1')
                num2 = form.cleaned_data.get('num2')
                num3 = form.cleaned_data.get('num3')
                num4 = form.cleaned_data.get('num4')
                num5 = form.cleaned_data.get('num5')
                num6 = form.cleaned_data.get('num6')
                code_insert = f'{num1}{num2}{num3}{num4}{num5}{num6}'
                if code_insert == user.active_code:
                    # user.is_active = True
                    user.token = get_random_string(100)
                    user.active_code = create_random_code(6)
                    user.save()
                    request.session['change-password'] = user.token
                    return redirect('change-password')
                else:
                    return render(request, 'active_user.html', {
                        'form_active': form,
                        'error': True
                    })
            else:
                return render(request, 'active_user.html', {
                    'form_active': form,
                    'error': True
                })
        else:
            return render(request, '404.html', {

            })


class ChangePasswordView(View):
    def get(self, request):
        try:
            cookie = request.session['change-password']
        except:
            cookie = None
        if cookie:
            return render(request, 'change-password.html', {

            })
        else:
            return render(request, '404.html', {

            })

    def post(self, request):
        try:
            cookie = request.session['change-password']
        except:
            cookie = None
        user = User.objects.filter(token=cookie).first()
        if user is not None:
            password = request.POST['pass1']
            re_password = request.POST['pass2']
            if password == re_password:
                if user.check_password(password):
                    return render(request, 'change-password.html', {
                        'oldpassword': True
                    })
                else:
                    user.set_password(password)
                    user.active_code = create_random_code(6)
                    user.token = get_random_string(100)
                    user.save()
                    return render(request, 'change-password.html', {
                        'success': True
                    })
            else:
                return render(request, 'change-password.html', {
                    'notmatch': True
                })


def log_out(request):
    user = request.user
    user.active_code = create_random_code(6)
    user.token = get_random_string(100)
    user.save()
    logout(request)
    return redirect('login')
