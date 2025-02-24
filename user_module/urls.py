from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *
urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('active-user/', ActiveUserView.as_view(), name='active-user'),
    path('forget-password/', ForgetPassword.as_view(), name='forget-password'),
    path('confirm-password/', ConfirmPasswordView.as_view(), name='confirm-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', log_out, name='logout'),
]