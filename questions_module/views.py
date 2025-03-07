from django.shortcuts import render
from django.views import View
from sitesetting_module.models import QuestionsModel


# Create your views here.
class QuestionsView(View):
    def get(self, request):
        settings = QuestionsModel.objects.filter(is_active=True).first()
        return render(request, 'questions.html', {
            "settings": settings,
        })