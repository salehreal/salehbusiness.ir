from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView
from cart_module.models import CartModel
from .forms import ContactUsForm, AvatarForm
from .models import ContactUsModel
from django.views import View
from .models import UploadAvatarModel
from sitesetting_module.models import SiteSettingModel
# Create your views here.

class ContactUsView(CreateView):
    template_name = 'contact.html'
    form_class = ContactUsForm
    success_url = '/'
    def get_context_data(self, **kwargs):
        context = super(ContactUsView, self).get_context_data(**kwargs)
        context["setting"] = SiteSettingModel.objects.filter(is_active=True).first()
        user = self.request.user
        cart = CartModel.objects.filter(user_id=user.id, is_paid=False).first()
        context['cart'] = cart
        return context

class UploadAvatarView(View):
    def get(self, request):
        av = AvatarForm()
        return render(request, 'upload_avatar.html', {
            'avatar': av,
        })
    def post(self, request:HttpRequest):
        av = AvatarForm(request.POST, request.FILES)
        if av.is_valid():
            image = av.cleaned_data.get('img')
            new_avatar = UploadAvatarModel(avatar=image)
            new_avatar.save()
            return render(request, 'upload_avatar.html')
