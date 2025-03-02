from django.urls import path
from . import views
from .views import add_to_wish, delete_wish_detail

urlpatterns = [
    path('' , views.WishView.as_view(), name='wish'),
    path('add-to-wish/', add_to_wish, name='add_to_wish'),
    path('delete-wish-detail/', delete_wish_detail, name='delete_wish_detail'),
]