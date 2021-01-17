from django.db import models
from datetime import datetime
from utils.BaseModels import BaseModel
# Create your models here.


class RemoteUser(BaseModel):
    name = models.CharField(max_length=32,verbose_name='名称')
    username = models.CharField(max_length=64,verbose_name='用户名')
    password = models.CharField(max_length=128,verbose_name='密码')
    enabled = models.BooleanField(default=False,verbose_name='是否su root')
    superuser = models.CharField(max_length=64,blank=True,null=True,verbose_name='超级用户')
    superpass = models.CharField(max_length=128,blank=True,null=True,verbose_name='特权密码')
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'remote_user'
        verbose_name = "主机账户"
        verbose_name_plural = verbose_name
        unique_together = (('name','username','password'),)

class RemoteUserBindHost(BaseModel):
    PROTOCOL_CHOICES = (
        (1,'ssh'),
        (2,'rdp'),
        (3,'vnc'),
        (4,'telnet')
    )
    TYPE_CHOICES = (
        (1,'服务器'),
        (2,'交换机'),
        (3,'虚拟机')
    )
    ENV_CHOICES = (
        (1,'product'),
        (2,'dev')
    )
    PLATFORM_CHOICES = (
        (1,'linux'),
        (2,'windows'),
        (3,'other')
    )
    hostname = models.CharField(max_length=128,verbose_name='主机名',unique=True,error_messages={'unique':'该主机已存在'})
    type = models.SmallIntegerField(default=1,choices=TYPE_CHOICES,verbose_name='类型')
    ip = models.GenericIPAddressField(verbose_name='IP',unique=True,error_messages={'unique':'该IP已存在'})
    protocol = models.SmallIntegerField(default=1,choices=PROTOCOL_CHOICES,verbose_name='协议')
    env = models.SmallIntegerField(default=1,choices=ENV_CHOICES,verbose_name='环境')
    host_group = models.ManyToManyField('HostGroup',verbose_name='主机组',blank=True,)
    port = models.SmallIntegerField(default=22,verbose_name='端口')
    release = models.CharField(max_length=128,default='Centos',verbose_name='系统')
    platform = models.SmallIntegerField(default=1,choices=PLATFORM_CHOICES,verbose_name='平台')
    # rdp 验证方式，可选项：rdp，tls，nla，nla-ext
    security = models.CharField(blank=True, null=True, max_length=32, verbose_name='rdp验证方式',help_text='rdp 验证方式，可选项：rdp，tls，nla，nla-ext')
    remote_user = models.ForeignKey('RemoteUser', blank=True, null=True, on_delete=models.PROTECT)
    enabled = models.BooleanField(default=True, verbose_name='是否启用')
    def __str__(self):
        return self.hostname
    class Meta:
        db_table = 'remoteuser_host'
        verbose_name = '主机绑定'
        verbose_name_plural = verbose_name


class Hosts(BaseModel):
    server = models.OneToOneField('RemoteUserBindHost',on_delete=models.CASCADE)
    cpu_number = models.SmallIntegerField(blank=True, null=True, verbose_name='物理CPU个数')
    vcpu_number = models.SmallIntegerField(blank=True, null=True, verbose_name='逻辑CPU个数')
    cpu_info = models.CharField(max_length=128, verbose_name='CPU', blank=True, null=True)
    os = models.CharField(max_length=64, blank=True, null=True, verbose_name='系统')
    os_kernel = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'系统内核')
    memory = models.CharField(max_length=12, verbose_name=u'内存/G', blank=True, null=True)
    disk = models.CharField(max_length=12, verbose_name=u'硬盘/G', blank=True, null=True)
    filesystems = models.TextField(blank=True, null=True, verbose_name='文件系统')
    interfaces = models.TextField(blank=True, null=True, verbose_name='网卡信息')
    server_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='型号')

    class Meta:
        db_table = 'hosts'
        verbose_name = u'主机'
        verbose_name_plural = verbose_name

class HostGroup(BaseModel):
    name = models.CharField(max_length=32,verbose_name=u'主机组名',unique=True,error_messages={'required':'主机名必须填写','unique':'该主机组已存在，请不要重复添加'})
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'hostgroup'
        verbose_name = u'主机组'
        verbose_name_plural = verbose_name


class CpuMonit(models.Model):
    # cpu监控
    # id自增,类型为bigint。设置为主键
    id = models.BigAutoField(primary_key=True)
    # 类型为decimal(10,2)，长度为10，小数点保留2位
    cpu = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="cpu使用率")
    # 类型为datetime
    create_time = models.DateTimeField(verbose_name="创建时间")
    # 由于毫秒的时间戳超过了timestamp的长度，所以只能设置bigint了。
    time_stamp = models.BigIntegerField(verbose_name="毫秒时间戳")
    host = models.ForeignKey(to='RemoteUserBindHost', on_delete=models.CASCADE)
    class Meta:
        db_table = 'cpumonit'
        verbose_name = u'cpu监控'
        verbose_name_plural = verbose_name

class MemoryMonit(models.Model):
    # 内存监控
    # id自增,类型为bigint。设置为主键
    id = models.BigAutoField(primary_key=True)
    # 类型为int(11)，11是默认长度
    cur_mem = models.IntegerField(verbose_name="当前使用内存")
    mem_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="内存使用率")
    mem_all = models.IntegerField(verbose_name="最大内存")
    # 类型为datetime
    create_time = models.DateTimeField(verbose_name="创建时间")
    # 由于毫秒的时间戳超过了timestamp的长度，所以只能设置bigint了。
    time_stamp = models.BigIntegerField(verbose_name="毫秒时间戳")
    host = models.ForeignKey(to='RemoteUserBindHost', on_delete=models.CASCADE)
    class Meta:
        db_table = 'memorymonit'
        verbose_name = u'内存监控'
        verbose_name_plural = verbose_name