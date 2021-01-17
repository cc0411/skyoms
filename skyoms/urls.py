"""skyoms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include,re_path
from django.views.static import serve
from .settings import MEDIA_ROOT
from rest_framework.documentation import include_docs_urls
from django.views.generic.base import TemplateView
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    # django默认认证
    path('api-auth/', include('rest_framework.urls')),
    #rest文档页
    path('docs/',include_docs_urls(title="skyoms")),
    path('users/', include('users.urls')),
    path('api/vms/',include('vms.urls')),
    path('api/assets/',include('assets.urls')),
    re_path('^favicon.ico$',RedirectView.as_view(url=r'static/favicon.ico')),
    #文件
    path('media/<path:path>',serve,{'document_root':MEDIA_ROOT}),
    re_path('', TemplateView.as_view(template_name='index.html')),
]
