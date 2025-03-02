from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from product_module.models import ProductModel
from wish_module.models import WishModel, WishDetailModel


# Create your views here.
class WishView(View):
    def get(self, request):
        user = request.user
        wish = WishModel.objects.filter(user_id=user.id).first()
        return render(request, 'wishlist.html', {
            'wish': wish,
        })

def add_to_wish(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        return JsonResponse({'status': "not_login"})
    try:
        product_id = int(request.GET.get("product_id"))
    except:
        return JsonResponse({'status': "error"})

    product = ProductModel.objects.filter(id=product_id).first()
    if not product:
        return JsonResponse({'status': "error"})

    wish, _ = WishModel.objects.get_or_create(user_id=user.id)
    detail = WishDetailModel.objects.filter(wish_id=wish.id, product_id=product_id).first()
    if detail is not None:
        detail.save()
    else:
        detail = WishDetailModel(wish_id=wish.id, product_id=product_id)
        detail.save()
    return JsonResponse({'status': "ok"})

@login_required
def delete_wish_detail(request):
    try:
        product_id = int(request.GET.get("detail_id"))
    except ValueError:
        return JsonResponse({'status': "error", 'message': "Invalid product_id"})
    detail = WishDetailModel.objects.filter(product_id=product_id, wish__user_id=request.user.id).first()
    if not detail:
        return JsonResponse({'status': "error", 'message': "Product not found"})
    detail.delete()
    wish = WishModel.objects.filter(user_id=request.user.id).first()
    updated_wish_list = WishDetailModel.objects.filter(wish=wish)
    return render(request, 'content-wishlist.html', {
        'wish': wish,
        'wish_details': updated_wish_list  # اطمینان از ارسال لیست به‌روزشده به قالب
    })
