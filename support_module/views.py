from django.shortcuts import render
from django.views import View
from sitesetting_module.models import SuppoertModel

# Create your views here.
class SupportView:
    def get(self, request):
        settings = SupportModel.objects.filter(is_active=True).first()
        return render(request, 'questions.html', {
            "settings": settings,
        })