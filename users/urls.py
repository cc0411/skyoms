# -*- coding:utf-8 -*-
from django.urls import re_path
from users.views import *
from rest_framework.routers import DefaultRouter
from .views import LoginRecordViewSet,CollectRecordViewSet,UserViewset, ChangeUserPasswdView, GroupsViewset, UserGroupViewset, GroupMemberViewset, \
    PermissionViewset, GroupPermViewset, PersonalInfoViewset
router = DefaultRouter()

router.register(r'loginrecord',LoginRecordViewSet,basename="loginrecord")
router.register(r'collectrecord',CollectRecordViewSet,basename="collectrecord")
router.register("personinfo", PersonalInfoViewset, basename="personinfo")
router.register("users", UserViewset, basename="users")
router.register("chuserpasswd", ChangeUserPasswdView, basename="chuserpasswd")
router.register("groups", GroupsViewset, basename="groups")
router.register("usergroup", UserGroupViewset, basename="usergroup")
router.register("groupmember", GroupMemberViewset, basename="groupmember")
router.register("permission", PermissionViewset, basename="permission")
router.register("groupperm", GroupPermViewset, basename="groupperm")

urlpatterns = [
    re_path('^login/$', user_login, name='login'),
    re_path('^captcha/(?P<image_uuid>[\w-]+)/$', user_captcha, name='captcha'),
    re_path('^list_user_menu/$', ListUserMenu.as_view(), name='list_user_menu'),
    re_path('^list_user_router/$', ListUserRouter.as_view(), name='list_user_router'),
]

urlpatterns += router.urls