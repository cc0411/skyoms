# -*- coding:utf-8 -*-

from django.urls import  re_path,path

from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$',consumers.ChatConsumer.as_asgi()),
    path('ws/cmd/', consumers.Cmd),
    path('ws/script/', consumers.Script),
    path('ws/file/', consumers.File),
    path('ws/playbook/', consumers.Playbook),
    path('ws/module/', consumers.Module),

]