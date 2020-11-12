# -*- coding:utf-8 -*-
from django.urls import re_path
from users.views import *
from rest_framework.routers import DefaultRouter
from .views import LoginRecordViewSet
router = DefaultRouter()

router.register(r'loginrecord',LoginRecordViewSet,basename="loginrecord")

urlpatterns = [
    re_path('login/', user_login, name='login'),
    re_path('captcha/(?P<image_uuid>[\w-]+)/', user_captcha, name='captcha'),
    re_path('list_user_menu/', ListUserMenu.as_view(), name='list_user_menu'),
    re_path('list_user_router/', ListUserRouter.as_view(), name='list_user_router'),
]

urlpatterns += router.urls