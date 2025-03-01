from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from cart_module.models import CartModel, CartDetailModel


# Create your views here.

@method_decorator(decorator=login_required, name='dispatch')
class MainDashboard(View):
    def get(self, request:HttpRequest):
        user = request.user
        user_carts = CartModel.objects.filter(user_id=user.id, is_paid=True)
        return render(request, 'my-account.html', {
            'user': user,
            'cart': user_carts,
        })

    def post(self, request:HttpRequest):
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        province = request.POST['province']
        old_pass = request.POST['old-password']
        new_pass = request.POST['new-password']
        re_new_pass = request.POST['re-new-password']
        user = request.user
        if user.check_password(old_pass):
            if new_pass == re_new_pass:
                user.first_name = first_name
                user.last_name = last_name
                user.province = province
                user.set_password(new_pass)
                user.save()
                return redirect('login')
        else:
            pass

@login_required
def detail_cart(request, id):
    details = CartDetailModel.objects.filter(cart_id=id)
    if len(details) > 0:
        return render(request, '', {
            'details': details,
        })