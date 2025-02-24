from django.urls import path
from .views import *

urlpatterns = [
    path('', ContactUsView.as_view(), name='contact-us'),
    path('upload-avatar/', UploadAvatarView.as_view(), name='upload-avatar'),
]