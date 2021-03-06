from .models import HostGroup,Hosts,RemoteUserBindHost,RemoteUser
from .serializer import HostGroupSerializer,HostSerializer,RemoteUserBindHostSerializer,RemoteUserSerializer
from utils.BaseViews import BaseView
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
# Create your views here.
from django.http import JsonResponse,HttpResponse
from .tasks import Update_host_info
from rest_framework.views import APIView
from skyoms.expiring_token_authentication import ExpireTokenAuthentication
import json


class HostGroupViewSet(BaseView):
    '''
    主机组
    '''
    queryset = HostGroup.objects.all().order_by("-ctime")
    serializer_class = HostGroupSerializer
    filter_fields = ['name',]
    search_fields = ('name',)
    ordering_fields = ('ctime','name')

class HostViewSet(BaseView):
    '''
    主机详细信息
    '''
    queryset = Hosts.objects.all().order_by("-ctime")
    serializer_class = HostSerializer
    filter_fields = ['cpu_info','os',]
    search_fields = ('os_kernel','os','server')
    ordering_fields = ('ctime','memory','cpuload','memorylimit','disk')

class RemoteUserViewSet(BaseView):
    '''
    主机远程账户
    '''
    queryset = RemoteUser.objects.all().order_by("-ctime")
    serializer_class = RemoteUserSerializer
    ordering_fields = ('ctime',)
    search_fields =('name',)
    filter_fields =('name',)


class RemoteUserBindHostViewSet(BaseView):
    '''
    主机绑定用户
    '''
    queryset = RemoteUserBindHost.objects.all().order_by("-ctime")
    serializer_class = RemoteUserBindHostSerializer
    ordering_fields = ('ctime',)
    search_fields = ('hostname','ip')
    filter_fields = ('enabled','env')

class Host2GroupViewset(viewsets.GenericViewSet,
                       mixins.UpdateModelMixin):
    """
    update:
        更新绑定主机的主机组信息
    """

    queryset = RemoteUserBindHost.objects.all().order_by('id')
    serializer_class = RemoteUserBindHostSerializer

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.host_group.set(request.data)

        return Response(status=status.HTTP_204_NO_CONTENT)

class HostGroupMemberViewset(viewsets.GenericViewSet,
                         mixins.DestroyModelMixin):
    """
    destory:
        删除主机组中的成员信息
    """
    queryset = HostGroup.objects.all().order_by('id')
    serializer_class = HostGroupSerializer

    def destroy(self, request, *args, **kwargs):
        group_obj = self.get_object()
        host_obj = RemoteUserBindHost.objects.get(id=request.data['id'])
        host_obj.host_group.remove(group_obj.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetHostGroup(APIView):
    '''
    自定义主机组分类
    '''
    def get(self,request):
        json_list = [
            {'value':0,'label':'所有主机'},
            {'value':-1,'label':'自定义'}
        ]
        groups = HostGroup.objects.all()
        for g in groups:
            json_dict = {}
            json_dict["value"] = g.id
            json_dict["label"] = g.name
            json_list.append(json_dict)
        return HttpResponse(json.dumps(json_list),content_type='application/json')

class GetGroup2Hosts(APIView):
    def get(self,request):
        json_list = []
        group = request.GET.get('hostgroup')
        if group == '0'  or group == '-1':
            host = RemoteUserBindHost.objects.all()
            print('111')
        else:
            host = RemoteUserBindHost.objects.filter(host_group__id=group)
        print(host)
        for h in  host:
            json_dict = {
                "value": h.id,
                "label": h.ip
            }
            json_list.append(json_dict)
        return HttpResponse(json.dumps(json_list),content_type='application/json')
    
class update_hostinfo(APIView):
    '''
    Ansible 更新主机硬件信息
    '''

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
