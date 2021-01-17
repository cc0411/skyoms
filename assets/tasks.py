# -*- coding:utf-8 -*-

from __future__ import absolute_import
from skyoms import celery_app
from skyoms import settings
import json
import os
from utils.Ansible_api import AnsibleAPI
from utils.callback import SetupCallbackModule,ModuleCallbackModule,CopyCallbackModule,PlayBookCallbackModule
from utils.inventory import BaseInventory
from assets.models import RemoteUserBindHost,Hosts
import random
import time
# 生成随机字符串
def gen_rand_char(length=16, chars='0123456789zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA'):
    return ''.join(random.sample(chars, length))

@celery_app.task()
def add(x,y):
    return x+y


@celery_app.task()
def Update_host_info(hostinfo):
    print("开始采集信息")
    host_data = [
        {
            'hostname': hostinfo['hostname'],
            'ip':hostinfo['ip'],
            'port':hostinfo['port'],
            'username':hostinfo['username'],
            'password':hostinfo['password']
        }
    ]
    if hostinfo['superusername']:
        host_data[0]['become'] = {
            'method':'su',
            'user':hostinfo['superusername'],
            'pass':hostinfo['superpassword']
        }
    print(host_data)
    inventory = BaseInventory(host_data)
    callback = SetupCallbackModule()
    ansible_api = AnsibleAPI(dynamic_inventory=inventory,callback=callback)

    server_info, failed, unreach, error = ansible_api.get_server_info(hosts='all')
    if server_info:
        host = RemoteUserBindHost.objects.get(pk=hostinfo['id'])
        data = {
            'server':host,
            'cpu_number':server_info[0]['cpu_number'],
            'vcpu_number':server_info[0]['vcpu_number'],
            'cpu_info':server_info[0]['cpu_model'],
            'os':server_info[0]['system'],
            'os_kernel':server_info[0]['kernel'],
            'memory':server_info[0]['ram_total'],
            'disk':server_info[0]['disk_total'],
            'filesystems':server_info[0]['filesystems'],
            'interfaces':server_info[0]['interfaces'],
            'server_model':server_info[0]['server_model'],
            #'cpuload':server_info[0]['cpuload'],
            #'memoryusage':server_info[0]['memusage'],
            #'memorylimit':server_info[0]['memorylimit']
        }
        print(data)
        Hosts.objects.update_or_create(server=host,defaults=data)

    else:
        if failed:
            for i in failed:
                print(json.dumps(i,indent=4))
        if unreach:
            for i in unreach:
                print(json.dumps(i,indent=4))
        if error:
            for i in error:
                print(json.dumps(i,indent=4))



@celery_app.task()
def Run_cmd(hosts,group,cmd,user,user_agent,client):
    host_data = list()
    _hosts = ''
    for host in hosts:
        _hosts += '{}_{}_{}\n'.format(host['hostname'],host['ip'],host['username'])
        hostinfo = dict()
        hostinfo['hostname'] = host['hostname']
        hostinfo['ip'] = host['ip']
        hostinfo['port'] = host['port']
        hostinfo['username'] = host['username']
        hostinfo['password'] = host['password']
        if host['superuser']:
            hostinfo['become'] = {
                'method': 'su',
                'user': host['superuser'],
                'pass': host['superpass']
            }
        host_data.append(hostinfo)
    inventory = BaseInventory(host_data)
    callback = ModuleCallbackModule(group,cmd=cmd,user=user,user_agent=user_agent,client=client,_hosts=_hosts)
    ansible_api = AnsibleAPI(dynamic_inventory=inventory,callback=callback)
    ansible_api.run_cmd(cmds=cmd,hosts='all',group=group)


@celery_app.task()
def Run_script(hosts,group,data,user,user_agent,client):
    host_data = list()
    _hosts = ''
    for host in hosts:
        _hosts += '{}_{}_{}\n'.format(host['hostname'], host['ip'], host['username'])
        hostinfo = dict()
        hostinfo['hostname'] = host['hostname']
        hostinfo['ip'] = host['ip']
        hostinfo['port'] = host['port']
        hostinfo['username'] = host['username']
        hostinfo['password'] = host['password']
        if host['superuser']:
            hostinfo['become'] = {
                'method': 'su',
                'user': host['superuser'],
                'pass': host['superpass']
            }
        host_data.append(hostinfo)
    inventory = BaseInventory(host_data)
    callback = ModuleCallbackModule(group,cmd=data['script_name'],user=user,user_agent=user_agent,client=client,_hosts=_hosts)
    ansible_api = AnsibleAPI(dynamic_inventory=inventory,callback=callback)
    path = data.get('path','/tmp')
    if path == '':
        path = '/tmp'
    exec = data.get('exec','')
    script_name = data.get('script_name','')
    script = data.get('script','')
    now =time.time()
    tmp_date = time.strftime("%Y-%m-%d", time.localtime(int(now)))
    if not os.path.isdir(os.path.join(settings.SCRIPT_ROOT, tmp_date)):
        os.makedirs(os.path.join(settings.SCRIPT_ROOT, tmp_date))
    script_file = settings.SCRIPT_DIR + '/' + tmp_date + '/' + gen_rand_char(16) + '_' + script_name
    res_file = settings.MEDIA_ROOT + '/' + script_file
    with open(res_file, 'w+') as f:
        f.write(script)
    cmds = '{}'.format(res_file)
    cmds = cmds + ' ' + 'chdir={}'.format(path)
    if exec:
        cmds = cmds + ' ' + 'executable={}'.format(exec)
    else:
        if script_name.split('.')[-1] == 'py':
            cmds = cmds + ' ' + 'executable=/usr/bin/python'
        elif script_name.split('.')[-1] == 'pl':
            cmds = cmds + ' ' + 'executable=/usr/bin/perl'
        elif script_name.split('.')[-1] == 'rb':
            cmds = cmds + ' ' + 'executable=/usr/bin/ruby'
    ansible_api.run_script(cmds=cmds, hosts='all', group=group, script=script_file)


@celery_app.task()
def Run_playbook(hosts, group, data, user, user_agent, client):
    host_data = list()
    _hosts = ''
    for host in hosts:
        _hosts += '{}_{}_{}\n'.format(host['hostname'], host['ip'], host['username'])
        hostinfo = dict()
        hostinfo['hostname'] = host['hostname']
        hostinfo['ip'] = host['ip']
        hostinfo['port'] = host['port']
        hostinfo['username'] = host['username']
        hostinfo['password'] = host['password']
        hostinfo['groups'] = host['groups'] if host['groups'] else None

        if host['superuser']:
            hostinfo['become'] = {
                'method': 'su',
                'user': host['superuser'],
                'pass': host['superpass']
                }
        host_data.append(hostinfo)
    inventory = BaseInventory(host_data)
    callback = PlayBookCallbackModule(group, playbook=data['playbook_name'], user=user, user_agent=user_agent,
                                      client=client, _hosts=_hosts)
    ansible_api = AnsibleAPI(
        dynamic_inventory=inventory,
        callback=callback
    )
    playbook_name = data.get('playbook_name', '')
    playbook = data.get('playbook', '')
    now = time.time()
    tmp_date = time.strftime("%Y-%m-%d", time.localtime(int(now)))
    if not os.path.isdir(os.path.join(settings.SCRIPT_ROOT, tmp_date)):
        os.makedirs(os.path.join(settings.SCRIPT_ROOT, tmp_date))
    script_file = settings.SCRIPT_DIR + '/' + tmp_date + '/' + gen_rand_char(16) + '_' + playbook_name
    playbook_file = settings.MEDIA_ROOT + '/' + script_file
    with open(playbook_file, 'w+') as f:
        f.write(playbook)
    ansible_api.run_playbook(playbook_yml=playbook_file, group=group, script=script_file)


@celery_app.task()
def Run_module(hosts, group, data, user, user_agent, client):
    host_data = list()
    _hosts = ''
    for host in hosts:
        _hosts += '{}_{}_{}\n'.format(host['hostname'], host['ip'], host['username'])
        hostinfo = dict()
        hostinfo['hostname'] = host['hostname']
        hostinfo['ip'] = host['ip']
        hostinfo['port'] = host['port']
        hostinfo['username'] = host['username']
        hostinfo['password'] = host['password']

        if host['superuser']:
            hostinfo['become'] = {
                'method': 'su',
                'user': host['superuser'],
                'pass': host['superpass']
                }
        host_data.append(hostinfo)
    inventory = BaseInventory(host_data)
    module = data.get('module', 'command')
    args = data.get('args', '')
    cmd = 'module: {0} args: {1}'.format(module, args)
    callback = ModuleCallbackModule(group, cmd=cmd, user=user, user_agent=user_agent, client=client, _hosts=_hosts)
    ansible_api = AnsibleAPI(
        dynamic_inventory=inventory,
        callback=callback
    )
    ansible_api.run_modules(cmds=args, module=module, hosts='all', group=group)


@celery_app.task()
def Run_file(hosts, group, data, user, user_agent, client):
    host_data = list()
    _hosts = ''
    for host in hosts:
        _hosts += '{}_{}_{}\n'.format(host['hostname'], host['ip'], host['username'])
        hostinfo = dict()
        hostinfo['hostname'] = host['hostname']
        hostinfo['ip'] = host['ip']
        hostinfo['port'] = host['port']
        hostinfo['username'] = host['username']
        hostinfo['password'] = host['password']
        if host['superuser']:
            hostinfo['become'] = {
                'method': 'su',
                'user': host['superuser'],
                'pass': host['superpass']
                }
        host_data.append(hostinfo)
    src = data.get('src')
    dst = data.get('dst', '/tmp')
    if dst == '':
        dst = '/tmp'
    backup = data.get('backup', True)
    cmds = 'src={} dest={} backup={} decrypt=False'.format(src, dst, backup)
    inventory = BaseInventory(host_data)
    callback = CopyCallbackModule(group, src=src, dst=dst, user=user, user_agent=user_agent, client=client, _hosts=_hosts)
    ansible_api = AnsibleAPI(
        dynamic_inventory=inventory,
        callback=callback
    )
    ansible_api.run_copy(cmds=cmds, hosts='all', group=group)
