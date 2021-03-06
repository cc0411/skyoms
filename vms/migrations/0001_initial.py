# Generated by Django 3.1.2 on 2020-10-31 16:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clusters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('ctime', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('utime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='集群名')),
                ('overallstatus', models.CharField(default='green', max_length=32, verbose_name='状态')),
                ('numshosts', models.SmallIntegerField(verbose_name='宿主机数量')),
                ('cputotal', models.CharField(max_length=64, verbose_name='CPU总计')),
                ('cpuusage', models.CharField(max_length=64, verbose_name='CPU使用量')),
                ('memtotal', models.CharField(max_length=64, verbose_name='内存总计')),
                ('memusage', models.CharField(max_length=64, verbose_name='内存使用量')),
                ('datatotal', models.CharField(max_length=64, verbose_name='存储总计')),
                ('datafree', models.CharField(max_length=64, verbose_name='存储剩余量')),
                ('vmscount', models.SmallIntegerField(verbose_name='虚拟机数量')),
            ],
            options={
                'verbose_name': '集群',
                'verbose_name_plural': '集群',
                'db_table': 'clusters',
            },
        ),
        migrations.CreateModel(
            name='DataCenters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('ctime', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('utime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='数据中心名')),
                ('cputotal', models.CharField(max_length=64, verbose_name='CPU总计')),
                ('cpuusage', models.CharField(max_length=64, verbose_name='CPU使用量')),
                ('memtotal', models.CharField(max_length=64, verbose_name='内存总计')),
                ('memusage', models.CharField(max_length=64, verbose_name='内存使用量')),
                ('datatotal', models.CharField(max_length=64, verbose_name='存储总计')),
                ('datafree', models.CharField(max_length=64, verbose_name='存储剩余量')),
                ('numhosts', models.SmallIntegerField(verbose_name='宿主机数量')),
                ('numcpuscores', models.SmallIntegerField(verbose_name='CPU总核数')),
                ('vmscount', models.SmallIntegerField(verbose_name='虚拟机数量')),
            ],
            options={
                'verbose_name': '数据中心',
                'verbose_name_plural': '数据中心',
                'db_table': 'data_centers',
            },
        ),
        migrations.CreateModel(
            name='DataStores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('ctime', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('utime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=32, verbose_name='存储名')),
                ('capacity', models.CharField(max_length=64, verbose_name='存储总量')),
                ('freespace', models.CharField(max_length=64, verbose_name='存储剩余')),
                ('datacenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vms.datacenters', verbose_name='数据中心')),
            ],
            options={
                'verbose_name': '存储',
                'verbose_name_plural': '存储',
                'db_table': 'datastores',
            },
        ),
        migrations.CreateModel(
            name='VirtualHosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('ctime', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('utime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=128, verbose_name='虚拟机名称')),
                ('ip', models.CharField(max_length=64, verbose_name='宿主机IP')),
                ('conState', models.CharField(max_length=32, verbose_name='连接状态')),
                ('powerState', models.CharField(max_length=32, verbose_name='电源状态')),
                ('cpunums', models.SmallIntegerField(verbose_name='CPU数量')),
                ('memtotal', models.CharField(max_length=32, verbose_name='总内存')),
                ('os', models.CharField(default='', max_length=64, verbose_name='系统名称')),
                ('cpuusage', models.CharField(max_length=32, verbose_name='CPU使用量')),
                ('memusage', models.CharField(max_length=32, verbose_name='内存使用量')),
                ('store_usage', models.CharField(max_length=32, verbose_name='存储使用量')),
                ('datacenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vms.datacenters')),
            ],
            options={
                'verbose_name': '虚拟机',
                'verbose_name_plural': '虚拟机',
                'db_table': 'virtualhosts',
            },
        ),
        migrations.CreateModel(
            name='NetworkAdapters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('ctime', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('utime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=64, verbose_name='分布式交换机名')),
                ('vlanid', models.CharField(max_length=32, verbose_name='VlanID')),
                ('type', models.CharField(max_length=32, verbose_name='类型')),
                ('datacenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vms.datacenters', verbose_name='数据中心')),
            ],
            options={
                'verbose_name': '网络端口',
                'verbose_name_plural': '网络端口',
                'db_table': 'networkadapters',
            },
        ),
        migrations.CreateModel(
            name='Dedicatedhosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('ctime', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('utime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='主机名')),
                ('conState', models.CharField(max_length=32, verbose_name='连接状态')),
                ('powerState', models.CharField(max_length=32, verbose_name='电源状态')),
                ('uuid', models.CharField(max_length=128, verbose_name='UUID')),
                ('cpumodel', models.CharField(max_length=128, verbose_name='CPU类型')),
                ('cpunums', models.SmallIntegerField(verbose_name='CPU数量')),
                ('cpucores', models.SmallIntegerField(verbose_name='CPU核数')),
                ('cputhreads', models.SmallIntegerField(verbose_name='CPU线程数')),
                ('cputotal', models.CharField(max_length=64, verbose_name='CPU总计')),
                ('cpuusage', models.CharField(max_length=64, verbose_name='CPU使用量')),
                ('memtotal', models.CharField(max_length=32, verbose_name='总内存')),
                ('memusage', models.CharField(max_length=32, verbose_name='内存使用数')),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vms.clusters', verbose_name='集群')),
                ('datacenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vms.datacenters', verbose_name='数据中心')),
                ('datastore', models.ManyToManyField(to='vms.DataStores', verbose_name='存储')),
            ],
            options={
                'verbose_name': '宿主机',
                'verbose_name_plural': '宿主机',
                'db_table': 'dedicatedhosts',
            },
        ),
        migrations.AddField(
            model_name='clusters',
            name='datacenter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vms.datacenters', verbose_name='数据中心'),
        ),
    ]
