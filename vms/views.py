from django.views import View
from django.http import HttpResponse
from .serializer import DataCentersSerializer,DataStoresSerializer,ClustersSerializer,NetworkAdaptersSerializer,DedicatedhostsSerializer,VirtualHostsSerializer
from .models import Dedicatedhosts,VirtualHosts,DataStores,DataCenters,Clusters,NetworkAdapters
from utils.BaseViews import BaseView


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
    ordering_fields = ('ctime','freespace')


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
            json_dict["cpu总计/GHz"] = float(re.sub('[^0-9.]',"",h.cputotal))
            json_dict["cpu已用/GHz"] = float(re.sub('[^0-9.]',"",h.cpuusage))
            json_dict["内存总计/G"] = float(re.sub('[^0-9.]',"",h.memtotal))
            json_dict["内存已用/G"] = float(re.sub('[^0-9.]',"",h.memusage))
            json_list.append(json_dict)
        return HttpResponse(json.dumps(json_list),content_type='application/json')


class GetDatastoreResource(View):
    '''
    获取存储使用率
    '''
    def get(self,request):
        datacenter = request.GET.get('datacenter')
        json_list =[]
        if datacenter:
            data = DataStores.objects.filter(datacenter__name=datacenter)
        else:
            data = DataStores.objects.all()
        for d in data:
            json_dict ={}
            totalspace = float(re.sub('[^0-9.]',"",d.capacity))
            freespace = float(re.sub('[^0-9.]',"",d.freespace))
            usagespace = totalspace-freespace
            json_dict["存储名"] = d.name
            json_dict["总空间"] = totalspace
            json_dict["剩余空间"] = freespace
            json_dict["使用率"] = "%.2f%%" %(usagespace/totalspace*100)
            json_list.append(json_dict)
        return HttpResponse(json.dumps(json_list), content_type='application/json')
