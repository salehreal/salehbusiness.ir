from django.urls import path
from .views import *


urlpatterns = [
    path("", MainDashboard.as_view(), name="main-dash"),
]