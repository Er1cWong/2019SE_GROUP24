"""djangoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path

from trying import views#导入views模块
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login),
    path('alarm/', views.alarm),
    url(r'^accounts/', include('trying.urls')),
    url(r'^index/',views.index),#配置当访问index/时去调用views下的index方法
    url(r'^study/',views.study),
    url(r'^show1/',views.show1),
    url(r'^show2/',views.show2),
    url(r'^show3/',views.show3),
    url(r'^show4/',views.show4),
    url(r'^AbnormalEvents/',views.AbnormalEvents),
    url(r'^HomePage/',views.HomePage)
]

urlpatterns += staticfiles_urlpatterns()
