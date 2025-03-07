from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestionsView.as_view(), name='questions'),
]