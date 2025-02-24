from django.shortcuts import render
from django.views import View
from sitesetting_module.models import AboutUsModel


# Create your views here.

class AboutUsView(View):
    def get(self, request):
        settings = AboutUsModel.objects.filter(is_active=True).first()
        return render(request, 'about-us.html', {
            "settings": settings,
        })
