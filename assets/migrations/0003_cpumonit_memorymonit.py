# Generated by Django 3.1.2 on 2020-12-10 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20201210_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemoryMonit',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cur_mem', models.IntegerField(verbose_name='当前使用内存')),
                ('mem_rate', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='内存使用率')),
                ('mem_all', models.IntegerField(verbose_name='最大内存')),
                ('create_time', models.DateTimeField(verbose_name='创建时间')),
                ('time_stamp', models.BigIntegerField(verbose_name='毫秒时间戳')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.remoteuserbindhost')),
            ],
        ),
        migrations.CreateModel(
            name='CpuMonit',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cpu', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='cpu使用率')),
                ('create_time', models.DateTimeField(verbose_name='创建时间')),
                ('time_stamp', models.BigIntegerField(verbose_name='毫秒时间戳')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.remoteuserbindhost')),
            ],
        ),
    ]
