# -*- coding:utf-8 -*-
from rest_framework import  serializers
from .models import HostGroup,Hosts,RemoteUserBindHost,RemoteUser
from utils.crypto import encrypt
class HostGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostGroup
        fields = ("id","name",'desc')
    def to_representation(self, instance):
        """
            序列化
            """
        ret = super(HostGroupSerializer, self).to_representation(instance)
        host_queryset = instance.remoteuserbindhost_set.all()
        host_list = []
        for host_obj in host_queryset:
            host_list.append({
                "id": host_obj.id,
                "hostname": host_obj.hostname,
                "type": host_obj.type,
                "ip": host_obj.ip,
                "protocol": host_obj.protocol,
                "env": host_obj.env,
                "port": host_obj.port,
                "release": host_obj.release,
                "security": host_obj.security,
                #"remote_user": host_obj.remote_user,
                "enabled": host_obj.enabled
            })
        ret['hosts'] = host_list
        return ret

class HostSerializer(serializers.ModelSerializer):
    server = serializers.SlugRelatedField(queryset=RemoteUserBindHost.objects.all(),
                                    slug_field='ip')
    class Meta:
        model = Hosts
        fields = '__all__'


class RemoteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemoteUser
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data.get('name')
        username = validated_data.get('username')
        password = encrypt(validated_data.get('password'))
        enabled = validated_data.get('enabled')
        superuser = validated_data.get('superuser')
        if validated_data.get('superpass'):
            superpass = encrypt(validated_data['superpass'])
        else:
            superpass = ""
        instance = RemoteUser.objects.create(name=name,password=password,
                                             username=username,enabled=enabled,
                                             superuser=superuser,
                                             superpass=superpass)
        instance.save()
        return instance
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.username = validated_data.get('username',instance.username)
        instance.enabled = validated_data.get('enabled',instance.enabled)
        if instance.password != validated_data.get('password'):

            instance.password = encrypt(validated_data.get('password'))
        else:
            instance.password = validated_data.get('password')
        instance.superuser = validated_data.get('superuser',instance.superuser)
        if instance.superpass !=validated_data.get('superpass'):
            instance.superpass = encrypt(validated_data['superpass'])
        else:
            instance.superpass = validated_data.get('superpass')
        instance.save()
        return instance

class RemoteUserBindHostSerializer(serializers.ModelSerializer):
    remote_user = serializers.SlugRelatedField(queryset=RemoteUser.objects.all(),slug_field='name')
    #ctime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", label="创建时间", help_text="创建时间", required=False,
    #                                        read_only=True)
    #utime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", label="更新时间", help_text="更新时间", required=False,
    #                                        read_only=True)
    class Meta:
        model = RemoteUserBindHost
        fields = ('id','hostname','ip','type','protocol','env','port','release','platform','security','remote_user','enabled')
    def to_representation(self, instance):
        ret = super(RemoteUserBindHostSerializer, self).to_representation(instance)
        group_queryset = instance.host_group.all()
        group_list = []
        for group_obj in group_queryset:
            group_list.append({
                "id": group_obj.id,
                "name": group_obj.name
            })
        ret['host_group'] = group_list
        return ret