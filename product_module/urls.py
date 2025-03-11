from django.urls import path
from . import views
from .views import send_product_comment, submit_comment_and_rating, ProductList, filter_products

urlpatterns = [
    path('', views.ProductList.as_view(), name='product-list'),
    path('detail/<slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug>/', views.category, name='product-category'),
    path('tags/<slug>', views.tags, name='tags'),
    path('submit-comment-and-rating/<slug:slug>/', submit_comment_and_rating, name='submit_comment_and_rating'),
    path('send-comment/<slug:slug>/', send_product_comment, name='send_product_comment'),
    path('products/', ProductList.as_view(), name='product_list'),
    path('filter-products/', filter_products, name='filter-products'),
]
