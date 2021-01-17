# -*- coding:utf-8 -*-
from ansible import constants as C  #获取内置常量
from ansible.module_utils.common.collections import ImmutableDict #自定制选项
from ansible import context  #上下文管理器，
from ansible.parsing.dataloader import DataLoader  #解析json/yaml文件
from ansible.vars.manager import VariableManager  #管理主机变量
from ansible.playbook.play import Play   #Ad-doc
from ansible.executor.task_queue_manager import TaskQueueManager   #任务队列管理
from ansible.executor.playbook_executor import PlaybookExecutor  #执行playbook
import json
import time
import traceback
import shutil
import os
import re
from skyoms import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
channel_layer = get_channel_layer()

def save_res(res_file, res):
    with open(settings.MEDIA_ROOT + '/' + res_file, 'a+') as f:
        for line in res:
            f.write('{}\n'.format(line))

class AnsibleAPI(object):

    def __init__(self,check=False,remote_user='root',private_key_file=None,forks=10,extra_vars=None,dynamic_inventory=None,callback=None):
        self.check = check
        self.private_key_file = private_key_file
        self.forks = forks
        self.remote_user = remote_user
        self.loader = DataLoader()
        self.passwords = {}
        self.results_callback = callback
        self.dynamic_inventory = dynamic_inventory
        self.variable_manager = VariableManager(loader=self.loader,inventory=self.dynamic_inventory)
        self.variable_manager._extra_vars = extra_vars if extra_vars is not None else {}
        self.__init_options()
    def __init_options(self):
        context.CLIARGS = ImmutableDict(
            connection = 'paramiko',
            remote_user = self.remote_user,
            ack_pass = None,
            sudo = True,
            sudo_user = 'root',
            ask_sudo_pass = False,
            module_path = None,
            become=True,
            become_method='sudo',
            become_user='root',
            check=self.check,
            listhosts=None,
            listtasks=None,
            listtags=None,
            syntax=None,
            diff=True,
            subset=None,
            timeout=15,
            private_key_file=self.private_key_file,
            host_key_checking=False,
            forks=self.forks,
            ssh_common_args='-o StrictHostKeyChecking=no',
            ssh_extra_args='-o StrictHostKeyChecking=no',
            verbosity=0,
            start_at_task=None,



        )
    def run_playbook(self,playbook_yml,group=None,script=None):
        playbook = None
        try:
            with open(playbook_yml) as f:
                playbook_content = f.read()
            playbook = PlaybookExecutor(
                    playbooks=[playbook_yml],
                    inventory=self.dynamic_inventory,
                    variable_manager=self.variable_manager,
                    loader=self.loader,
                    passwords=self.passwords,
                )
            playbook._tqm._stdout_callback = self.results_callback
            playbook.run()
        except Exception as err:
            data = '<code style="color: #FF0000">{}</code>'.format(str(err))
            data2 = '\033[01;31m{}\r\n\r\n\033[0m'.format(str(err).strip().replace('\n', '\r\n'))
            delay = round(time.time() - self.results_callback.start_time, 6)
            self.results_callback.res.append(json.dumps([delay, 'o', data2]))
            message = dict()
            message['status'] = 0
            message['message'] = data
            message = json.dumps(message)
            async_to_sync(channel_layer.group_send)(group, {
                "type": "send.message",
                "text": message,
            })
        finally:
            if group:
                message = dict()
                message['status'] = 0
                message['message'] = '执行完毕...'
                message = json.dumps(message)
                async_to_sync(channel_layer.group_send)(group, {
                    "type": "close.channel",
                    "text": message,
                })
                if self.results_callback.res:
                    save_res(self.results_callback.res_file, self.results_callback.res)
                    #batchcmd_log(
                    #    user=self.results_callback.user,
                    #    hosts=self.results_callback.hosts,
                    #    cmd=self.results_callback.playbook,
                    #    detail=self.results_callback.res_file,
                    #    address=self.results_callback.client,
                    #    useragent=self.results_callback.user_agent,
                    #    start_time=self.results_callback.start_time_django,
                    #    type=4,
                    #    script=script,
                    #)
            if playbook._tqm is not None:
                playbook._tqm.cleanup()

    def run_module(self,module_name,module_args,hosts='all'):
        play_source = dict(
            name='Ansible Run Module',
            hosts=hosts,
            gather_facts='no',
            tasks=[
                {'action': {'module': module_name, 'args': module_args}},
            ]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.dynamic_inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                passwords=self.passwords,
                stdout_callback=self.results_callback,
            )
            tqm.run(play)
            # self.result_row = self.results_callback.result_row
        except Exception:
            print(traceback.format_exc())
        finally:
            if tqm is not None:
                tqm.cleanup()
            # 这个临时目录会在 ~/.ansible/tmp/ 目录下
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def run_modules(self, cmds, module='command', hosts='all', group=None):
        try:
            module_name = module
            self.run_module(module_name, cmds, hosts)
        except Exception as err:
            data = '<code style="color: #FF0000">{}</code>'.format(str(err))
            data2 = '\033[01;31m{}\r\n\r\n\033[0m'.format(str(err).strip().replace('\n', '\r\n'))
            delay = round(time.time() - self.results_callback.start_time, 6)
            self.results_callback.res.append(json.dumps([delay, 'o', data2]))
            message = dict()
            message['status'] = 0
            message['message'] = data
            message = json.dumps(message)
            async_to_sync(channel_layer.group_send)(group, {
                "type": "send.message",
                "text": message,
            })
        finally:
            if group:
                message = dict()
                message['status'] = 0
                message['message'] = '执行完毕...'
                message = json.dumps(message)
                async_to_sync(channel_layer.group_send)(group, {
                    "type": "close.channel",
                    "text": message,
                })
                if self.results_callback.res:
                    save_res(self.results_callback.res_file, self.results_callback.res)
                    #batchcmd_log(
                    #    user=self.results_callback.user,
                    #    hosts=self.results_callback.hosts,
                    #    cmd=self.results_callback.cmd,
                    #    detail=self.results_callback.res_file,
                    #    address=self.results_callback.client,
                    #    useragent=self.results_callback.user_agent,
                    #    start_time=self.results_callback.start_time_django,
                    #    type=5,
                    #)

    def run_cmd(self, cmds, hosts='all', group=None):
        try:
            module_name = 'shell'
            self.run_module(module_name, cmds, hosts)
        except Exception as err:
            data = '<code style="color: #FF0000">{}</code>'.format(str(err))
            data2 = '\033[01;31m{}\r\n\r\n\033[0m'.format(str(err).strip().replace('\n', '\r\n'))
            delay = round(time.time() - self.results_callback.start_time, 6)
            self.results_callback.res.append(json.dumps([delay, 'o', data2]))
            message = dict()
            message['status'] = 0
            message['message'] = data
            message = json.dumps(message)
            async_to_sync(channel_layer.group_send)(group, {
                "type": "send.message",
                "text": message,
            })
        finally:
            if group:
                message = dict()
                message['status'] = 0
                message['message'] = '执行完毕...'
                message = json.dumps(message)
                async_to_sync(channel_layer.group_send)(group, {
                    "type": "close.channel",
                    "text": message,
                })
                if self.results_callback.res:
                    save_res(self.results_callback.res_file, self.results_callback.res)
                    #batchcmd_log(
                    #    user=self.results_callback.user,
                    #    hosts=self.results_callback.hosts,
                    #    cmd=self.results_callback.cmd,
                    #    detail=self.results_callback.res_file,
                    #    address=self.results_callback.client,
                    #    useragent=self.results_callback.user_agent,
                    #    start_time=self.results_callback.start_time_django,
                    #)

    def run_script(self, cmds, hosts='all', group=None, script=None):
        try:
            module_name = 'script'
            self.run_module(module_name, cmds, hosts)
        except Exception as err:
            data = '<code style="color: #FF0000">{}</code>'.format(str(err))
            data2 = '\033[01;31m{}\r\n\r\n\033[0m'.format(str(err).strip().replace('\n', '\r\n'))
            delay = round(time.time() - self.results_callback.start_time, 6)
            self.results_callback.res.append(json.dumps([delay, 'o', data2]))
            message = dict()
            message['status'] = 0
            message['message'] = data
            message = json.dumps(message)
            async_to_sync(channel_layer.group_send)(group, {
                "type": "send.message",
                "text": message,
            })
        finally:
            if group:
                message = dict()
                message['status'] = 0
                message['message'] = '执行完毕...'
                message = json.dumps(message)
                async_to_sync(channel_layer.group_send)(group, {
                    "type": "close.channel",
                    "text": message,
                })
                if self.results_callback.res:
                    save_res(self.results_callback.res_file, self.results_callback.res)
                    #batchcmd_log(
                    #    user=self.results_callback.user,
                    #    hosts=self.results_callback.hosts,
                    #    cmd=self.results_callback.cmd,
                    #    detail=self.results_callback.res_file,
                    #    address=self.results_callback.client,
                    #    useragent=self.results_callback.user_agent,
                    #    start_time=self.results_callback.start_time_django,
                    #    type=2,
                    #    script=script,
                    #)

    def run_copy(self, cmds, hosts='all', group=None):
        try:
            module_name = 'copy'
            self.run_module(module_name, cmds, hosts)
        except Exception as err:
            data = '<code style="color: #FF0000">{}</code>'.format(str(err))
            data2 = '\033[01;31m{}\r\n\r\n\033[0m'.format(str(err).strip().replace('\n', '\r\n'))
            delay = round(time.time() - self.results_callback.start_time, 6)
            self.results_callback.res.append(json.dumps([delay, 'o', data2]))
            message = dict()
            message['status'] = 0
            message['message'] = data
            message = json.dumps(message)
            async_to_sync(channel_layer.group_send)(group, {
                "type": "send.message",
                "text": message,
            })
        finally:
            if group:
                message = dict()
                message['status'] = 0
                message['message'] = '执行完毕...'
                message = json.dumps(message)
                async_to_sync(channel_layer.group_send)(group, {
                    "type": "close.channel",
                    "text": message,
                })
                if self.results_callback.res:
                    save_res(self.results_callback.res_file, self.results_callback.res)
                    #batchcmd_log(
                    #    user=self.results_callback.user,
                    #    hosts=self.results_callback.hosts,
                    #    cmd='上传文件 {} 到 {}'.format(self.results_callback.src.split('/')[-1], self.results_callback.dst),
                    #    detail=self.results_callback.res_file,
                    #    address=self.results_callback.client,
                    #   useragent=self.results_callback.user_agent,
                    #    start_time=self.results_callback.start_time_django,
                    #    type=3,
                    #)
            try:
                os.remove(self.results_callback.src)
            except Exception:
                print(traceback.format_exc())

    def get_server_info(self, hosts='all'):
        """
        获取主机信息
        """
        self.run_module('setup', '', hosts)
        ok, failed, unreach, error = self.results_callback.get_res()
        infos = []
        if ok:
            for i in ok:
                info = dict()
                info['host'] = i['host']
                info['hostname'] = i['result']['ansible_facts']['ansible_hostname']
                info['cpuload'] =i['result']['ansible_facts']['ansible_local']['resourcelimit']['cpuload']
                info['memusage'] = i['result']['ansible_facts']['ansible_local']['resourcelimit']['memusage']
                info['memorylimit'] = i['result']['ansible_facts']['ansible_local']['resourcelimit']['memorylimit']
                info['cpu_model'] = i['result']['ansible_facts']['ansible_processor'][-1]
                info['cpu_number'] = int(i['result']['ansible_facts']['ansible_processor_count'])
                info['vcpu_number'] = int(i['result']['ansible_facts']['ansible_processor_vcpus'])
                info['kernel'] = i['result']['ansible_facts']['ansible_kernel']
                info['system'] = '{} {} {}'.format(i['result']['ansible_facts']['ansible_distribution'],
                                                   i['result']['ansible_facts']['ansible_distribution_version'],
                                                   i['result']['ansible_facts']['ansible_userspace_architecture'])
                info['server_model'] = i['result']['ansible_facts']['ansible_product_name']
                info['ram_total'] = round(int(i['result']['ansible_facts']['ansible_memtotal_mb']) / 1024)
                info['swap_total'] = round(int(i['result']['ansible_facts']['ansible_swaptotal_mb']) / 1024)
                info['disk_total'], disk_size = 0, 0
                for k, v in i['result']['ansible_facts']['ansible_devices'].items():
                    if k[0:2] in ['sd', 'hd', 'ss', 'vd']:
                        if 'G' in v['size']:
                            disk_size = float(v['size'][0: v['size'].rindex('G') - 1])
                        elif 'T' in v['size']:
                            disk_size = float(v['size'][0: v['size'].rindex('T') - 1]) * 1024
                        info['disk_total'] += round(disk_size, 2)
                info['filesystems'] = []
                for filesystem in i['result']['ansible_facts']['ansible_mounts']:
                    tmp = dict()
                    tmp['mount'] = filesystem['mount']
                    tmp['size_total'] = filesystem['size_total']
                    tmp['size_available'] = filesystem['size_available']
                    tmp['fstype'] = filesystem['fstype']
                    info['filesystems'].append(tmp)

                info['interfaces'] = []
                interfaces = i['result']['ansible_facts']['ansible_interfaces']
                for interface in interfaces:
                    # lvs 模式时 lo 也可能会绑定 IP 地址
                    if re.match(r"^(eth|bond|bind|eno|ens|em|ib)\d+?", interface) or interface == 'lo':
                        tmp = dict()
                        tmp['network_card_name'] = i['result']['ansible_facts']['ansible_{}'.format(interface)].get(
                            'device')
                        tmp['network_card_mac'] = i['result']['ansible_facts']['ansible_{}'.format(interface)].get(
                            'macaddress')
                        tmp['network_card_ipv4'] = i['result']['ansible_facts']['ansible_{}'.format(interface)].get(
                            'ipv4') if 'ipv4' in i['result']['ansible_facts'][
                            'ansible_{}'.format(interface)] else 'unknown'

                        tmp['network_card_ipv4_secondaries'] = i['result']['ansible_facts'][
                            'ansible_{}'.format(interface)].get(
                            'ipv4_secondaries') if 'ipv4_secondaries' in i['result']['ansible_facts'][
                            'ansible_{}'.format(interface)] else 'unknown'

                        tmp['network_card_ipv6'] = i['result']['ansible_facts']['ansible_{}'.format(interface)].get(
                            'ipv6') if 'ipv6' in i['result']['ansible_facts'][
                            'ansible_{}'.format(interface)] else 'unknown'

                        tmp['network_card_model'] = i['result']['ansible_facts']['ansible_{}'.format(interface)].get(
                            'type')
                        tmp['network_card_mtu'] = i['result']['ansible_facts']['ansible_{}'.format(interface)].get(
                            'mtu')
                        tmp['network_card_status'] = i['result']['ansible_facts']['ansible_{}'.format(interface)].get(
                            'active')
                        tmp['network_card_speed'] = i['result']['ansible_facts']['ansible_{}'.format(interface)].get(
                            'speed')
                        info['interfaces'].append(tmp)
                infos.append(info)
        print('------------------')
        print(infos)
        return infos, failed, unreach, error

    def get_result(self):
        ok, failed, unreach, error = self.results_callback.get_res()

        if ok:
            print('ok-------------------start')
            for i in ok:
                print(json.dumps(i, indent=4))
            print('ok-------------------end')

        if failed:
            print('failed-------------------start')
            for i in failed:
                print(json.dumps(i, indent=4))
            print('failed-------------------end')

        if unreach:
            print('unreach-------------------start')
            for i in unreach:
                print(json.dumps(i, indent=4))
            print('unreach-------------------end')

        if error:
            print('error-------------------start')
            print(error)
            print('error-------------------end')


if __name__ == '__main__':
    host_data = [
        {
            'hostname' :'web1',
            'ip':'192.168.57.3',
            'port':22,
            'username':'cc0411',
            'password':'12345678',
            'groups':['web','db'],
            'become': {
                'method': 'su',
                'user': 'root',
                'pass': '123456',
            },

        },
        {
            'hostname': 'k8s1_test',
            'ip': '192.168.223.111',
            'port': 22,
            'username': 'test',
            'password': '123456',
            'groups': ['k8s'],
            'become': {
                'method': 'su',
                'user': 'root',
                'pass': '123456',
            },
        },
        {
            'hostname': 'testserver',
            'ip': '8.8.8.8',
            'port': 2222,
            'username': 'root',
            'password': 'password',
            'private_key': '/tmp/private_key',
            'become': {
                'method': 'sudo',
                'user': 'root',
                'pass': None,
            },
            'groups': ['group1', 'group2'],
            'vars': {'love': 'yes'},
        },
    ]
    playbook_yml = './hello.yml'
    private_key_file = './id_rsa'
    remote_user = 'root'
    extra_vars = {
        'var': 'test'
    }
    from utils.inventory import  BaseInventory

    inventory = BaseInventory(host_data)
    from utils.callback import CallbackModule, PlayBookCallbackModule

    callback = CallbackModule()
    #callback2 = PlayBookCallbackModule('saddasd', cmd='xx', user='admin', user_agent='admin',
    #                                   client='192.168.223.1', _hosts='192.168.223.111')
    ansible_api = AnsibleAPI(
        # private_key_file=private_key_file,
        # extra_vars=extra_vars,
        # remote_user=remote_user,
        dynamic_inventory=inventory,
        callback=callback,
        # forks=4,
    )

    #ansible_api.run_playbook(playbook_yml=playbook_yml)
    # ansible_api.run_module(module_name="shell", module_args="echo 'hello world!';echo $?", hosts="group1,group3")
    # cmd = '. /etc/profile &> /dev/null; . ~/.bash_profile &> /dev/null; ip a;'
    #ansible_api.run_module(module_name='shell', module_args="w", hosts='all')
    # ansible_api.run_cmd(cmds=cmd, hosts='k8s')
    # ansible_api.run_module(module_name='setup', module_args='', hosts='k8s')
    ansible_api.get_server_info(hosts='web1')
    ansible_api.get_result()
