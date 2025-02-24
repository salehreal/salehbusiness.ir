from django.urls import path
from .views import *


urlpatterns = [
    path('', BlogListView.as_view(), name='blog-list'),
    path('blog/<id>/', BlogDetailView.as_view(), name='blog-detail'),
    path('send-comment/', send_comment)
]