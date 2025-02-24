from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
# Create your views here.

@method_decorator(decorator=login_required, name='dispatch')
class MainDashboard(View):
    def get(self, request:HttpRequest):
        user = request.user
        return render(request, 'my-account.html', {
            'user': user,
        })