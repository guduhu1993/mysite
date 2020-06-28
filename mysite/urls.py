"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from blog.views import blog_list
from .views import home,login,register,logout,user_info,update_email,ImageCodeView
from django.conf.urls.static import static
from django.conf import settings
from blog.views import search
from rest_framework_jwt.views import obtain_jwt_token
from mysite.views import Verify


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include("blog.urls")),
    path('', home, name='home'),
    path('mdeditor/', include('mdeditor.urls')),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('user_info/', user_info, name='user_info'),
    path('update_email/', update_email, name='update_email'),
    path('comment/', include('comment.urls')),
    # path('search/', search, name='search'),
    path('search/', include('haystack.urls')),# 导入haystack应用的urls.py
    #path('get_token/', obtain_jwt_token),
    path('image_codes/<int:pic_id>', ImageCodeView.as_view(), name='image_codes'),
    path('verify/', Verify, name='verify'),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
