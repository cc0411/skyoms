# -*- coding:utf-8 -*-
from __future__ import absolute_import
from skyoms import celery_app
import time
from vms.models import *

from vms.utils.vmapi import VcenterApi
from django.core.exceptions import ObjectDoesNotExist


@celery_app.task
def CollectDatacenterinfo(host,user,pwd):
    print('开始采集数据中心' + time.strftime('%Y年%m月%d日 %X'))
    Vc=VcenterApi(host=host,user=user,pwd=pwd)
    v = Vc.get_datacenter_list()
    name = v['datacentername']
    numhosts = v['numhosts']
    cputotal = v['cputotal']
    cpuusage = v['cpuusage']
    memtotal = v['memtotal']
    memusage = v['memusage']
    datatotal = v['totaldatastore']
    datafree = v['datastorefree']
    numcpuscores = v['numcpucores']
    vmscount = v['vmcount']
    update_values = {'name': name,'numhosts': numhosts, 'cputotal': cputotal,
                             'cpuusage': cpuusage, 'memusage': memusage, 'memtotal': memtotal,
                             'datatotal': datatotal, 'datafree': datafree, 'vmscount': vmscount,
                             'numcpuscores':numcpuscores}
    DataCenters.objects.update_or_create(name=name,defaults=update_values)
    return "Datacenter---%s数据采集成功" %host

@celery_app.task
def CollectClusterinfo(host,user,pwd):
    print('开始采集集群信息' + time.strftime('%Y年%m月%d日 %X'))
    Vc=VcenterApi(host=host,user=user,pwd=pwd)
    res = Vc.get_cluster_list()
    for item in res:
        name = item.get('clustername')
        numshosts = item.get('numhosts')
        cputotal = item.get('cputotal')
        cpuusage = item.get('cpuusage')
        memtotal = item.get('memtotal')
        memusage = item.get('memusage')
        overallstatus = item.get('overallstatus')
        datatotal = item.get('totaldatastore')
        datafree = item.get('datastorefree')
        vmscount = item.get('vmcount')
        datacentername = item.get('datacentername')
        datacenter = DataCenters.objects.get(name=datacentername)
        update_values = {'name': name,'numshosts': numshosts, 'cputotal': cputotal,'overallstatus':overallstatus,
                             'cpuusage': cpuusage, 'memusage': memusage, 'memtotal': memtotal,
                             'datatotal': datatotal, 'datafree': datafree, 'vmscount': vmscount,
                             'datacenter':datacenter}
        Clusters.objects.update_or_create(name=name,defaults=update_values)
    return "Cluster-----%s数据采集成功"  %host

@celery_app.task
def CollectDatastoreinfo(host,user,pwd):
    print('开始采集存储信息' + time.strftime('%Y年%m月%d日 %X'))
    Vc=VcenterApi(host=host,user=user,pwd=pwd)
    res = Vc.get_datastore_list()
    for item in res:
        name = item.get('name')
        capacity = item.get('capacity')
        freespace = item.get('freespace')
        datacentername = item.get('datacentername')
        datacenter = DataCenters.objects.get(name=datacentername)
        update_values = {'name': name, 'capacity': capacity, 'freespace': freespace,
                             'datacenter':datacenter}
        DataStores.objects.update_or_create(name=name,defaults=update_values)
    return "Datastore------%s数据采集成功" %host

@celery_app.task
def CollectNetworkinfo(host,user,pwd):
    print('开始采集网络信息列表' + time.strftime('%Y年%m月%d日 %X'))
    Vc=VcenterApi(host=host,user=user,pwd=pwd)
    res = Vc.get_networkport_group_list()
    for item in res:
        name = item.get('name')
        vlanid = item.get('vlanid')
        type = item.get('type')
        datacentername = item.get('datacentername')
        datacenter = DataCenters.objects.get(name=datacentername)
        update_values = {'name': name, 'vlanid': vlanid, 'type': type,
                             'datacenter':datacenter}
        NetworkAdapters.objects.update_or_create(name=name,defaults=update_values)
    return "Network-----%s数据采集成功"  %host

@celery_app.task
def CollectVirtualinfo(host,user,pwd):
    print("开始采集虚拟机信息" +time.strftime('%Y年%m月%d日 %X' ))
    Vc = VcenterApi(host=host,user=user,pwd=pwd)
    res = Vc.get_vm_list()
    for item in res:
        name = item.get('name')
        datacentername = item.get('datacentername')
        datacenter = DataCenters.objects.get(name=datacentername)
        hostname = item.get('host')
        host = Dedicatedhosts.objects.get(name=hostname)
        ipaddr = item.get('ipaddress')
        if ipaddr is None:
            ip = ''
        else:
            ip = ipaddr
        conState = item.get('connectionstate')
        powerState = item.get('powerstate')
        cpunums = item.get('numcpu')
        memtotal = item.get('memtotal')
        os = item.get('os')
        cpuusage = item.get('cpuusage')
        memusage = item.get('memusage')
        store_usage = item.get('storage_usage')
        status = item.get('overallstatus')
        update_values = {'name':name,'datacenter':datacenter,'host':host,'ip':ip,
                        'conState':conState,'powerState':powerState,'cpuusage':cpuusage,
                        'cpunums':cpunums,'memusage':memusage,'memtotal':memtotal,
                        'os':os,'store_usage':store_usage,'status':status}
        VirtualHosts.objects.update_or_create(name=name,defaults=update_values)


    return  "Virtual-----%s数据采集成功"  %host

@celery_app.task
def CollectPhysicsinfo(host,user,pwd):
    print("开始采集宿主机信息"+time.strftime('%Y年%m月%d日 %X' ))
    Vc = VcenterApi(host=host,user=user,pwd=pwd)
    res = Vc.get_host_list()
    for item in res:
        name = item.get("name")
        datacentername = item.get('datacentername')
        datacenter = DataCenters.objects.get(name=datacentername)
        clustername = item.get('clustername')
        cluster = Clusters.objects.get(name=clustername)
        datastore = item.get("datastore")
        conState = item.get('connectionstate')
        powerState = item.get("powerstate")
        uuid = item.get("uuid")
        cpumodel = item.get("cpumodel")
        vendor = "%s--%s" %(item.get("vendor"),item.get("model"))
        cpunums = item.get("numcpupkgs")
        cpucores = item.get("numcpucores")
        cputhreads = item.get("numcputhreads")
        cputotal = item.get("cpusize")
        cpuusage = item.get("cpuusage")
        memtotal = item.get("memorysize")
        memusage = item.get("memusage")
        status = item.get("overallStatus")
        datastore_obj = DataStores.objects.filter(name__in=datastore)
        os = item.get("os")
        try:
            obj = Dedicatedhosts.objects.get(name=name)
        except ObjectDoesNotExist:
            obj =Dedicatedhosts.objects.create(name=name,datacenter=datacenter,cluster=cluster,
                                               conState=conState,powerState=powerState,uuid=uuid,
                                               cpumodel=cpumodel,vendor=vendor,cpunums=cpunums,
                                               cpucores=cpucores,cputhreads=cputhreads,cputotal=cputotal,
                                               cpuusage=cpuusage,memtotal=memtotal,memusage=memusage,
                                               status=status,os=os)
            obj.datastore.add(*datastore_obj)
            obj.save()
        else:

            obj=Dedicatedhosts.objects.filter(name=name)
            obj.update(datacenter=datacenter, cluster=cluster,
                                                conState=conState, powerState=powerState, uuid=uuid,
                                                cpumodel=cpumodel, vendor=vendor, cpunums=cpunums,
                                                cpucores=cpucores, cputhreads=cputhreads, cputotal=cputotal,
                                                cpuusage=cpuusage, memtotal=memtotal, memusage=memusage,
                                                status=status, os=os)
            obj.first().datastore.set(datastore_obj)
            obj.first().save()
    return "Physicsinfo----%s采集成功"  %host