"""
URL configuration for Config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('home_module.urls')),
    path("products/", include('product_module.urls')),
    path("contact-us/", include('contact_module.urls')),
    path("users/", include('user_module.urls')),
    path("blog/", include('blog_module.urls')),
    path('cart/', include('cart_module.urls')),
    path("about-us/", include('aboutus_module.urls')),
    path('user-panel/', include("user_dashboard_module.urls")),
    path("wish-list/", include("wish_module.urls")),
    path("asked-question/", include("questions_module.urls")),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
