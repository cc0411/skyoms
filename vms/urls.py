# -*- coding:utf-8 -*-
from rest_framework.routers import DefaultRouter
from vms.views import DataCentersViewSet,ClustersViewSet,DataStoresViewSet,NetworkAdaptersViewSet,DedicatedhostsViewSet,VirtualHostsViewSet
from django.urls import re_path
from .views import GetClusterHost,GetDedicatedhostResource,GetDatacenterTreeData,GetSystemData

router = DefaultRouter()

#vms
router.register(r'datacenter',DataCentersViewSet,basename="datacenter")
router.register(r'cluster',ClustersViewSet,basename="cluster")
router.register(r'datastore',DataStoresViewSet,basename="datastore")
router.register(r'networkadapter',NetworkAdaptersViewSet,basename="networkadapter")
router.register(r'dedicatedhost',DedicatedhostsViewSet,basename="dedicatedhost")
router.register(r'virtualhost',VirtualHostsViewSet,basename="virtualhost")


urlpatterns = [
   re_path('^getclusterhost/$',GetClusterHost.as_view(),name='getclusterhost'),
   re_path('^gethostresource/$',GetDedicatedhostResource.as_view(),name='gethostresource'),
   re_path('^gettreedata/$',GetDatacenterTreeData.as_view(),name='gettreedata'),
   re_path('^getsystemdata/$',GetSystemData.as_view(),name='getsystemdata'),

]
urlpatterns += router.urls