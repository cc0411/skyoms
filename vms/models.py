from django.db import models
from datetime import datetime
from utils.BaseModels import BaseModel
# Create your models here.

class DataCenters(BaseModel):
    '''数据中心'''
    name = models.CharField(max_length=128,verbose_name=u'数据中心名',unique=True)
    cputotal = models.CharField(max_length=64,verbose_name=u'CPU总计')
    cpuusage = models.CharField(max_length=64,verbose_name=u'CPU使用量')
    memtotal = models.CharField(max_length=64,verbose_name=u'内存总计')
    memusage = models.CharField(max_length=64,verbose_name=u'内存使用量')
    datatotal = models.CharField(max_length=64,verbose_name=u'存储总计')
    datafree  = models.CharField(max_length=64,verbose_name=u'存储剩余量')
    numhosts = models.SmallIntegerField(verbose_name=u'宿主机数量')
    numcpuscores = models.SmallIntegerField(verbose_name=u'CPU总核数')
    vmscount = models.SmallIntegerField(verbose_name=u'虚拟机数量')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'data_centers'
        verbose_name = u"数据中心"
        verbose_name_plural = verbose_name

class Clusters(BaseModel):
    '''集群'''
    name = models.CharField(max_length=128,verbose_name=u'集群名',unique=True)
    datacenter = models.ForeignKey('DataCenters',verbose_name=u'数据中心',on_delete=models.CASCADE)
    overallstatus = models.CharField(max_length=32,verbose_name=u'状态',default="green")
    numshosts = models.SmallIntegerField(verbose_name=u'宿主机数量')
    cputotal = models.CharField(max_length=64, verbose_name=u'CPU总计')
    cpuusage = models.CharField(max_length=64, verbose_name=u'CPU使用量')
    memtotal = models.CharField(max_length=64, verbose_name=u'内存总计')
    memusage = models.CharField(max_length=64, verbose_name=u'内存使用量')
    datatotal = models.CharField(max_length=64, verbose_name=u'存储总计')
    datafree = models.CharField(max_length=64, verbose_name=u'存储剩余量')
    vmscount = models.SmallIntegerField(verbose_name=u'虚拟机数量')
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'clusters'
        verbose_name = u'集群'
        verbose_name_plural = verbose_name

class DataStores(BaseModel):
    '''存储'''
    name = models.CharField(max_length=32,verbose_name=u'存储名')
    datacenter = models.ForeignKey('DataCenters', verbose_name=u"数据中心",on_delete=models.CASCADE)
    capacity = models.CharField(max_length=64,verbose_name=u'存储总量')
    freespace = models.CharField(max_length=64,verbose_name=u'存储剩余')

    def __str__(self):
        return self.name


    class Meta:
        db_table = 'datastores'
        verbose_name = u'存储'
        verbose_name_plural = verbose_name

class NetworkAdapters(BaseModel):
    '''网络'''
    name = models.CharField(max_length=64,verbose_name=u'分布式交换机名')
    datacenter = models.ForeignKey('DataCenters', verbose_name=u'数据中心',on_delete=models.CASCADE)
    vlanid = models.CharField(max_length=32,verbose_name=u'VlanID')
    type = models.CharField(max_length=32,verbose_name=u'类型')
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'networkadapters'
        verbose_name = u'网络端口'
        verbose_name_plural = verbose_name

class Dedicatedhosts(BaseModel):
    '''宿主机'''
    name = models.GenericIPAddressField(verbose_name=u'主机名',unique=True)
    cluster = models.ForeignKey('Clusters',verbose_name=u'集群',on_delete=models.CASCADE)
    datacenter = models.ForeignKey(DataCenters,verbose_name="数据中心",on_delete=models.CASCADE)
    datastore = models.ManyToManyField('DataStores',verbose_name=u'存储')
    conState = models.CharField(max_length=32,verbose_name=u'连接状态')
    powerState = models.CharField(max_length=32,verbose_name=u'电源状态')
    uuid = models.CharField(max_length=128,verbose_name=u'UUID')
    cpumodel = models.CharField(max_length=128,verbose_name=u'CPU类型')
    vendor = models.CharField(max_length=64,verbose_name='厂商',default='')
    cpunums = models.SmallIntegerField(verbose_name=u'CPU数量')
    cpucores = models.SmallIntegerField(verbose_name=u'CPU核数')
    cputhreads = models.SmallIntegerField(verbose_name=u'CPU线程数')
    cputotal = models.CharField(max_length=64, verbose_name=u'CPU总计')
    cpuusage = models.CharField(max_length=64, verbose_name=u'CPU使用量')
    memtotal = models.CharField(max_length=32,verbose_name=u'总内存')
    memusage = models.CharField(max_length=32,verbose_name=u'内存使用数')
    status = models.CharField(max_length=32,default='green',verbose_name=u'状态')
    os = models.CharField(max_length=64,verbose_name='系统',default='')
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'dedicatedhosts'
        verbose_name = u'宿主机'
        verbose_name_plural = verbose_name

class VirtualHosts(BaseModel):
    '''虚拟机'''
    name = models.CharField(max_length=128,verbose_name=u'虚拟机名称')
    ip = models.GenericIPAddressField(max_length=64,verbose_name=u'IP',blank=True,null=True)
    host = models.ForeignKey('Dedicatedhosts',on_delete=models.CASCADE,default=None)
    datacenter = models.ForeignKey('DataCenters',on_delete=models.CASCADE)
    conState = models.CharField(max_length=32,verbose_name=u'连接状态')
    powerState = models.CharField(max_length=32,verbose_name=u'电源状态')
    cpunums = models.SmallIntegerField(verbose_name=u'CPU数量')
    memtotal = models.CharField(max_length=32,verbose_name=u'总内存')
    os = models.CharField(max_length=64,verbose_name=u'系统名称',default='')
    cpuusage = models.CharField(max_length=32,verbose_name=u'CPU使用量')
    memusage = models.CharField(max_length=32,verbose_name=u'内存使用量')
    store_usage = models.CharField(max_length=32,verbose_name=u'存储使用量')
    status = models.CharField(max_length=32,verbose_name='状态',default='green')

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'virtualhosts'
        verbose_name_plural = u'虚拟机'
        verbose_name = verbose_name_plural
