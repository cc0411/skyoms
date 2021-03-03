# -*- coding:utf-8 -*-
from rest_framework.routers import DefaultRouter
from assets.views import HostGroupViewSet,HostViewSet,RemoteUserBindHostViewSet,RemoteUserViewSet,Host2GroupViewset
from django.urls import re_path
from .monitor import cpu,memory
from django.views.decorators.csrf import csrf_exempt
from .views import update_hostinfo,GetHostGroup
router = DefaultRouter()



router.register(r'host',HostViewSet,basename="host")
router.register(r'remoteuser',RemoteUserViewSet,basename="remoteuser")
router.register(r'userbindhost',RemoteUserBindHostViewSet,basename="userbindhost")
router.register(r'hostgroup',HostGroupViewSet,basename="hostgroup")
router.register("host2group", Host2GroupViewset, basename="host2group")
urlpatterns = [
    re_path('^update_hostinfo/$',update_hostinfo.as_view(),name='update_hostinfo'),
    re_path('^gethostgroup/$',GetHostGroup.as_view(),name='gethostgroup'),
    re_path(r'cpu/add/$', cpu.CpuView.as_view({'post': 'add'}), name='cpu'),
    re_path(r'memory/add/$', memory.MemoryView.as_view({'post': 'add'}), name='memory'),

    re_path(r'cpu/chart_json/(?P<pk>\d+)/$', cpu.CpuView.as_view({'get': 'chart_json'}), name='chart_cpu'),
    re_path(r'memory/chart_json/(?P<pk>\d+)/$', memory.MemoryView.as_view({'get': 'chart_json'}), name='chart_memory'),
]
urlpatterns += router.urls