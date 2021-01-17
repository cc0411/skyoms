from .models import HostGroup,Hosts,RemoteUserBindHost,RemoteUser
from .serializer import HostGroupSerializer,HostSerializer,RemoteUserBindHostSerializer,RemoteUserSerializer
from utils.BaseViews import BaseView
# Create your views here.
from django.http import JsonResponse,HttpResponse
from .tasks import Update_host_info
from rest_framework.views import APIView
from skyoms.expiring_token_authentication import ExpireTokenAuthentication
import json


class HostGroupViewSet(BaseView):
    queryset = HostGroup.objects.all().order_by("-ctime")
    serializer_class = HostGroupSerializer
    filter_fields = ['name',]
    search_fields = ('name',)
    ordering_fields = ('ctime','name')

class HostViewSet(BaseView):
    queryset = Hosts.objects.all().order_by("-ctime")
    serializer_class = HostSerializer
    filter_fields = ['cpu_info','os',]
    search_fields = ('os_kernel','os','server')
    ordering_fields = ('ctime','memory','cpuload','memorylimit','disk')

class RemoteUserViewSet(BaseView):
    queryset = RemoteUser.objects.all().order_by("-ctime")
    serializer_class = RemoteUserSerializer
    ordering_fields = ('ctime',)
    search_fields =('name',)
    filter_fields =('name',)


class RemoteUserBindHostViewSet(BaseView):
    queryset = RemoteUserBindHost.objects.all().order_by("-ctime")
    serializer_class = RemoteUserBindHostSerializer
    ordering_fields = ('ctime',)
    search_fields = ('hostname','ip')
    filter_fields = ('enabled','env')

class GetHostGroup(APIView):
    def get(self,request):
        json_list = []
        data = HostGroup.objects.all()
        data1= RemoteUserBindHost.objects.all()
        json_dict1 = {}
        json_dict1['value'] = 0
        json_dict1['label'] = '所有主机'
        json_list.append(json_dict1)
        json_dict2 = {}
        json_dict2['value'] = -1
        json_dict2['label'] = '自定义'
        json_list.append(json_dict2)
        for d in data:
            json_dict = {}
            json_dict["value"] = d.id
            json_dict["label"] = d.name
            json_list.append(json_dict)


        return HttpResponse(json.dumps(json_list),content_type='application/json')


class update_hostinfo(APIView):

    authentication_classes = (ExpireTokenAuthentication,)
    def post(self,request):
        result = {
            'code': 0,
            'msg': '',
            'data': {}
        }
        hostid = request.data.get('id', None)
        hosts = RemoteUserBindHost.objects.filter(id=int(hostid), platform=1)
        if not hosts:
            result['code'] = 1
            result['msg'] = '主机未获取到'
            return JsonResponse(result)

        for host in hosts:
            hostinfo = dict()
            hostinfo["id"] = host.id
            hostinfo["hostname"] = host.hostname
            hostinfo["ip"] = host.ip
            hostinfo["port"] = host.port
            hostinfo["platform"] = host.get_platform_display()
            hostinfo["username"] = host.remote_user.username
            hostinfo["password"] = host.remote_user.password
            if host.remote_user.enabled:
                hostinfo["superusername"] = host.remote_user.superuser
                hostinfo["superpassword"] = host.remote_user.superpass
            else:
                hostinfo["superusername"] = None


            Update_host_info.delay(hostinfo=hostinfo)

        result['msg'] = '更新成功'
        return JsonResponse(result)