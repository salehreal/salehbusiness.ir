from django.contrib.auth import login, logout
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views import View
from .models import User
from utils.utils import create_random_code
from .forms import ActiveForm

# Create your views here.

class Register(View):
    def get(self, request):
        return render(request, 'register-page.html', {

        })
    def post(self, request: HttpRequest):
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        user = User.objects.filter(phone=phone).first()
        if user is not None:
            return render(request, 'register-page.html', {
                'exist': True
            })
        else:
            if len(str(username.strip())) > 2 and len(str(email.strip())) > 6 and len(str(phone.strip())) > 10 and len(str(password.strip())) > 5:
                new_user = User(username=username, email=email, phone=phone, active_code=create_random_code(6), token=get_random_string(100), is_active=False)
                new_user.set_password(raw_password=password)
                new_user.save()
                request.session['user_token'] = new_user.token
                request.session.set_expiry(190)
                # send_sms(new_user.phone, new_user.active_code)
                return redirect('active-user')
            else:
                return render(request, 'register-page.html', {
                    'error' : True
                })

class Login(View):
    def get(self, request):
        return render(request, 'login-page.html', {

        })
    def post(self, request):
        phone = request.POST['phone']
        password = request.POST['password']
        user = User.objects.filter(phone=phone).first()
        if user is not None:
            if user.check_password(password):
                login(request, user)
                return redirect('home')
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
        phone = request.POST['phone']
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
                'existError' : True
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
                'form_active' : form
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
                        'oldpassword' : True
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
