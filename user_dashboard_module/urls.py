from django.urls import path
from .views import *


urlpatterns = [
    path("main-dashboard/", MainDashboard.as_view(), name="main-dash"),
    # path('detail/<id>/', )
]