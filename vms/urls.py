# -*- coding:utf-8 -*-
from rest_framework.routers import DefaultRouter
from vms.views import DataCentersViewSet,ClustersViewSet,DataStoresViewSet,NetworkAdaptersViewSet,DedicatedhostsViewSet,VirtualHostsViewSet
from django.urls import path
from .views import GetClusterHost,GetDedicatedhostResource,GetDatastoreResource,GetDatacenterTreeData

router = DefaultRouter()

#vms
router.register(r'datacenter',DataCentersViewSet,basename="datacenter")
router.register(r'cluster',ClustersViewSet,basename="cluster")
router.register(r'datastore',DataStoresViewSet,basename="datastore")
router.register(r'networkadapter',NetworkAdaptersViewSet,basename="networkadapter")
router.register(r'dedicatedhost',DedicatedhostsViewSet,basename="dedicatedhost")
router.register(r'virtualhost',VirtualHostsViewSet,basename="virtualhost")


urlpatterns = [
   path('getclusterhost/',GetClusterHost.as_view(),name='getclusterhost'),
   path('gethostresource/',GetDedicatedhostResource.as_view(),name='gethostresource'),
   path('getdataresource/',GetDatastoreResource.as_view(),name='getdataresource'),
   path('gettreedata/',GetDatacenterTreeData.as_view(),name='gettreedata'),

]
urlpatterns += router.urls