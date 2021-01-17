from django.views import View
from django.http import HttpResponse
from .serializer import DataCentersSerializer,DataStoresSerializer,ClustersSerializer,NetworkAdaptersSerializer,DedicatedhostsSerializer,VirtualHostsSerializer
from .models import Dedicatedhosts,VirtualHosts,DataStores,DataCenters,Clusters,NetworkAdapters
from utils.BaseViews import BaseView
from django.db.models import  Count

class DataCentersViewSet(BaseView):
    queryset = DataCenters.objects.all().order_by("-ctime")
    serializer_class = DataCentersSerializer
    search_fields = ('name',)
    ordering_fields = ("ctime","numhosts","vmscount","datafree")

class ClustersViewSet(BaseView):
    queryset = Clusters.objects.all().order_by("-ctime")
    serializer_class = ClustersSerializer
    filter_fields = ['datacenter__name','overallstatus']
    search_fields = ('name',)
    ordering_fields = ('ctime','vmscount','numshosts','datafree',)


class DataStoresViewSet(BaseView):
    queryset = DataStores.objects.all().order_by("-ctime")
    serializer_class = DataStoresSerializer
    filter_fields = ['datacenter__name',]
    search_fields = ('name',)
    ordering_fields = ('ctime','freespace',)


class NetworkAdaptersViewSet(BaseView):
    queryset = NetworkAdapters.objects.all().order_by("-ctime")
    serializer_class = NetworkAdaptersSerializer
    filter_fields = ['datacenter__name',]
    search_fields = ('name',)
    #ordering_fields = ('ctime','name')



class DedicatedhostsViewSet(BaseView):
    queryset = Dedicatedhosts.objects.all().order_by("-ctime")
    serializer_class = DedicatedhostsSerializer
    filter_fields = ['cluster__name','datacenter__name','powerState','conState','status']
    search_fields = ('name',)
    ordering_fields = ('ctime','memusage','cpuusage','cputhreads')


class VirtualHostsViewSet(BaseView):
    queryset = VirtualHosts.objects.all().order_by("-ctime")
    serializer_class = VirtualHostsSerializer
    filter_fields = ['datacenter__name','host__name','powerState','conState','status']
    search_fields = ('name','ip')
    ordering_fields = ('ctime','memtotal','store_usage')

import json
class GetClusterHost(View):
    '''
    列出所有群集中虚拟机和宿主机的数量，前端Dashboard展示
    '''
    def get(self,request):
        json_list =[]
        datacenter = request.GET.get('datacenter')
        if datacenter:
            clusters = Clusters.objects.filter(datacenter__name=datacenter)
        else:
            clusters = Clusters.objects.all()
        for c in clusters:
            json_dict ={}
            json_dict["集群"] = c.name
            json_dict["宿主机数量"] = c.numshosts
            json_dict["虚拟机数量"] = c.vmscount
            json_list.append(json_dict)
        return HttpResponse(json.dumps(json_list),content_type='application/json')

import re
class GetDedicatedhostResource(View):
    '''
    列出宿主机内存、cpu使用量，用于Dashboard展示
    '''
    def get(self,request):
        json_list = []
        datacenter = request.GET.get('datacenter')
        if datacenter:
            hosts = Dedicatedhosts.objects.filter(datacenter__name=datacenter)
        else:
            hosts = Dedicatedhosts.objects.all()
        for h in  hosts:
            json_dict ={}
            json_dict["主机名"] = h.name
            json_dict["cpu总计/GHz"] = h.cputotal
            json_dict["cpu已用/GHz"] = h.cpuusage
            json_dict["内存总计/G"] = h.memtotal
            json_dict["内存已用/G"] = h.memusage
            json_list.append(json_dict)
        return HttpResponse(json.dumps(json_list),content_type='application/json')



class GetDatacenterTreeData(View):
    '''
    获取所有数据中心列表用于前端过滤
    '''
    def get(self,request):
        json_list = []
        data = DataCenters.objects.all()
        for d in data:
            json_dict = {}
            json_dict["value"] = d.name
            json_dict["label"] = d.name
            json_list.append(json_dict)
        return  HttpResponse(json.dumps(json_list),content_type='application/json')


class GetSystemData(View):
    '''
    获取系统分类数据

    '''
    def get(self,request):
        json_list =[]
        datacenter = request.GET.get('datacenter')
        if datacenter:
            vhosts = VirtualHosts.objects.values('os').annotate(count=Count('os')).filter(datacenter__name=datacenter)
        else:
            vhosts = VirtualHosts.objects.values('os').annotate(count=Count('os'))
        for v  in vhosts:
            json_dict = {}
            json_dict["系统类型"] = v['os']
            json_dict["数量"] = v['count']
            json_list.append(json_dict)
        return HttpResponse(json.dumps(json_list), content_type='application/json')