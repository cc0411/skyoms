# -*- coding:utf-8 -*-
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings
from .models import RemoteUserBindHost
from users.models import UserProfile
from django.db.models import Q
from asgiref.sync import async_to_sync
from utils.tools import gen_rand_char
from .tasks import Run_file ,Run_script,Run_module,Run_playbook,Run_cmd
import json,time,traceback


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
    def disconnect(self, code):
        self.close()
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({'message':message}))


def get_hosts(ids):
    return RemoteUserBindHost.objects.filter(Q(enabled=True),Q(id__in=ids.split(','))).distinct()



class Cmd(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = 'session_' + gen_rand_char()
        self.message = dict()
        self.client = None
        self.user_agent = None
        self.is_running = False

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(self.group, self.channel_name)  # 加入组
        for i in self.scope['headers']:
            if i[0].decode('utf-8') == 'user-agent':
                self.user_agent = i[1].decode('utf-8')
                break
        for i in self.scope['headers']:
            if i[0].decode('utf-8') == 'x-real-ip':
                self.client = i[1].decode('utf-8')
                break
            if i[0].decode('utf-8') == 'x-forwarded-for':
                self.client = i[1].decode('utf-8').split(',')[0]
                break
            self.client = self.scope['client'][0]

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(self.group, self.channel_name)  # 退出组
        except Exception:
            pass

    def receive(self, text_data=None, bytes_data=None):
        if self.is_running:
            self.message['status'] = 1
            self.message['message'] = '当前通道已有任务在执行'
            message = json.dumps(self.message)
            async_to_sync(self.channel_layer.group_send)(self.group, {
                "type": "send.message",
                "text": message,
            })
        else:
            self.is_running = True
            data = dict()
            try:
                data = json.loads(text_data)
            except Exception:
                self.message['status'] = 1
                self.message['message'] = '提交的数据格式错误'
                message = json.dumps(self.message)
                async_to_sync(self.channel_layer.group_send)(self.group, {
                    "type": "close.channel",
                    "text": message,
                })
            if data.get('hosts', None) and data.get('cmd', None):
                hosts = get_hosts(data['hosts'],)
                if not hosts:
                    self.message['status'] = 1
                    self.message['message'] = '未找到主机'
                    message = json.dumps(self.message)
                    async_to_sync(self.channel_layer.group_send)(self.group, {
                        "type": "close.channel",
                        "text": message,
                    })

                ansible_hosts = list()
                for host in hosts:
                    hostinfo = dict()
                    hostinfo['id'] = host.id
                    hostinfo['hostname'] = host.hostname
                    hostinfo['ip'] = host.ip
                    hostinfo['port'] = host.port
                    hostinfo['username'] = host.remote_user.username
                    hostinfo['password'] = host.remote_user.password
                    if host.remote_user.enabled:
                        hostinfo['superusername'] = host.remote_user.superuser
                        hostinfo['superpassword'] = host.remote_user.superpass
                    else:
                        hostinfo['superusername'] = None
                    ansible_hosts.append(hostinfo)
                Run_cmd.delay(
                    hosts=ansible_hosts, group=self.group,
                    cmd=data['cmd'],
                    user=self.scope.get('username'),
                    user_agent=self.user_agent,
                    client=self.client,
                )  # 执行

            else:
                self.message['status'] = 1
                self.message['message'] = '提交的数据格式错误'
                message = json.dumps(self.message)
                async_to_sync(self.channel_layer.group_send)(self.group, {
                    "type": "close.channel",
                    "text": message,
                })

    def send_message(self, data):
        try:
            self.send(data['text'])
        except Exception:
            print("send message error: {0}".format(traceback.format_exc()))
            #logger.error("send message error: {0}".format(traceback.format_exc()))

    def close_channel(self, data):
        try:
            self.send(data['text'])
            time.sleep(0.3)
            self.close()
        except Exception:
            #logger.error("close channel error: {0}".format(traceback.format_exc()))
            print("close channel error: {0}".format(traceback.format_exc()))

class Script(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = 'session_' + gen_rand_char()
        self.message = dict()
        self.client = None
        self.user_agent = None
        self.is_running = False

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(self.group, self.channel_name)  # 加入组

        for i in self.scope['headers']:
            if i[0].decode('utf-8') == 'user-agent':
                self.user_agent = i[1].decode('utf-8')
                break
        for i in self.scope['headers']:
            if i[0].decode('utf-8') == 'x-real-ip':
                self.client = i[1].decode('utf-8')
                break
            if i[0].decode('utf-8') == 'x-forwarded-for':
                self.client = i[1].decode('utf-8').split(',')[0]
                break
            self.client = self.scope['client'][0]

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(self.group, self.channel_name)  # 退出组
        except Exception:
            print(traceback.format_exc())

    def receive(self, text_data=None, bytes_data=None):
        if self.is_running:
            self.message['status'] = 1
            self.message['message'] = '当前通道已有任务在执行'
            message = json.dumps(self.message)
            async_to_sync(self.channel_layer.group_send)(self.group, {
                "type": "send.message",
                "text": message,
            })
        else:
            self.is_running = True
            data = dict()
            try:
                data = json.loads(text_data)
            except Exception:
                self.message['status'] = 1
                self.message['message'] = '提交的数据格式错误'
                message = json.dumps(self.message)
                async_to_sync(self.channel_layer.group_send)(self.group, {
                    "type": "close.channel",
                    "text": message,
                })
            if data.get('hosts', None) and data.get('script', None) and data.get('script_name', None):
                hosts = get_hosts(data['hosts'])
                if not hosts:
                    self.message['status'] = 1
                    self.message['message'] = '未找到主机'
                    message = json.dumps(self.message)
                    async_to_sync(self.channel_layer.group_send)(self.group, {
                        "type": "close.channel",
                        "text": message,
                    })

                ansible_hosts = list()
                for host in hosts:
                    hostinfo = dict()
                    hostinfo['id'] = host.id
                    hostinfo['hostname'] = host.hostname
                    hostinfo['ip'] = host.ip
                    hostinfo['port'] = host.port
                    hostinfo['username'] = host.remote_user.username
                    hostinfo['password'] = host.remote_user.password
                    if host.remote_user.enabled:
                        hostinfo['superusername'] = host.remote_user.superuser
                        hostinfo['superpassword'] = host.remote_user.superpass
                    else:
                        hostinfo['superusername'] = None
                    ansible_hosts.append(hostinfo)
                Run_script.delay(
                    hosts=ansible_hosts, group=self.group,
                    data=data,
                    user=self.scope.get('username'),
                    user_agent=self.user_agent,
                    client=self.client,
                )  # 执行

            else:
                self.message['status'] = 1
                self.message['message'] = '提交的数据格式错误'
                message = json.dumps(self.message)
                async_to_sync(self.channel_layer.group_send)(self.group, {
                    "type": "close.channel",
                    "text": message,
                })

    def send_message(self, data):
        try:
            self.send(data['text'])
        except Exception:
            print(traceback.format_exc())

    def close_channel(self, data):
        try:
            self.send(data['text'])
            time.sleep(0.3)
            self.close()
        except Exception:
            print(traceback.format_exc())

class File(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = 'session_' + gen_rand_char()
        self.message = dict()
        self.client = None
        self.user_agent = None
        self.is_running = False

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(self.group, self.channel_name)  # 加入组
        for i in self.scope['headers']:
            if i[0].decode('utf-8') == 'user-agent':
                self.user_agent = i[1].decode('utf-8')
                break
        for i in self.scope['headers']:
            if i[0].decode('utf-8') == 'x-real-ip':
                self.client = i[1].decode('utf-8')
                break
            if i[0].decode('utf-8') == 'x-forwarded-for':
                self.client = i[1].decode('utf-8').split(',')[0]
                break
            self.client = self.scope['client'][0]

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(self.group, self.channel_name)  # 退出组
        except Exception:
            print(traceback.format_exc())

    def receive(self, text_data=None, bytes_data=None):
        if self.is_running:
            self.message['status'] = 1
            self.message['message'] = '当前通道已有任务在执行'
            message = json.dumps(self.message)
            async_to_sync(self.channel_layer.group_send)(self.group, {
                "type": "send.message",
                "text": message,
            })
        else:
            self.is_running = True
            data = dict()
            try:
                data = json.loads(text_data)
            except Exception:
                self.message['status'] = 1
                self.message['message'] = '提交的数据格式错误'
                message = json.dumps(self.message)
                async_to_sync(self.channel_layer.group_send)(self.group, {
                    "type": "close.channel",
                    "text": message,
                })
            if ('hosts' in data) and ('src' in data) and ('dst' in data) and ('backup' in data):
                if not data['src'].startswith(settings.TMP_ROOT):
                    self.message['status'] = 1
                    self.message['message'] = '无权限的源文件'
                    message = json.dumps(self.message)
                    async_to_sync(self.channel_layer.group_send)(self.group, {
                        "type": "close.channel",
                        "text": message,
                    })
                hosts = get_hosts(data['hosts'])
                if not hosts:
                    self.message['status'] = 1
                    self.message['message'] = '未找到主机'
                    message = json.dumps(self.message)
                    async_to_sync(self.channel_layer.group_send)(self.group, {
                        "type": "close.channel",
                        "text": message,
                    })

                ansible_hosts = list()
                for host in hosts:
                    hostinfo = dict()
                    hostinfo['id'] = host.id
                    hostinfo['hostname'] = host.hostname
                    hostinfo['ip'] = host.ip
                    hostinfo['port'] = host.port
                    hostinfo['username'] = host.remote_user.username
                    hostinfo['password'] = host.remote_user.password
                    if host.remote_user.enabled:
                        hostinfo['superusername'] = host.remote_user.superuser
                        hostinfo['superpassword'] = host.remote_user.superpass
                    else:
                        hostinfo['superusername'] = None
                    ansible_hosts.append(hostinfo)
                Run_file.delay(
                    hosts=ansible_hosts, group=self.group,
                    data=data,
                    user=self.scope.get('username'),
                    user_agent=self.user_agent,
                    client=self.client,

                )  # 执行
            else:
                self.message['status'] = 1
                self.message['message'] = '提交的数据格式错误'
                message = json.dumps(self.message)
                async_to_sync(self.channel_layer.group_send)(self.group, {
                    "type": "close.channel",
                    "text": message,
                })

    def send_message(self, data):
        try:
            self.send(data['text'])
        except Exception:
            print(traceback.format_exc())

    def close_channel(self, data):
        try:
            self.send(data['text'])
            time.sleep(0.3)
            self.close()
        except Exception:
            print(traceback.format_exc())

class Playbook(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = 'session_' + gen_rand_char()
        self.message = dict()
        self.client = None
        self.user_agent = None
        self.is_running = False

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(self.group, self.channel_name)  # 加入组
        for i in self.scope['headers']:
            if i[0].decode('utf-8') == 'user-agent':
                self.user_agent = i[1].decode('utf-8')
                break
        for i in self.scope['headers']:
            if i[0].decode('utf-8') == 'x-real-ip':
                self.client = i[1].decode('utf-8')
                break
            if i[0].decode('utf-8') == 'x-forwarded-for':
                self.client = i[1].decode('utf-8').split(',')[0]
                break
            self.client = self.scope['client'][0]

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(self.group, self.channel_name)  # 退出组
        except Exception:
            print(traceback.format_exc())

    def receive(self, text_data=None, bytes_data=None):
        if self.is_running:
            self.message['status'] = 1
            self.message['message'] = '当前通道已有任务在执行'
            message = json.dumps(self.message)
            async_to_sync(self.channel_layer.group_send)(self.group, {
                "type": "send.message",
                "text": message,
            })
        else:
            self.is_running = True
            data = dict()
            try:
                data = json.loads(text_data)
            except Exception:
                self.message['status'] = 1
                self.message['message'] = '提交的数据格式错误'
                message = json.dumps(self.message)
                async_to_sync(self.channel_layer.group_send)(self.group, {
                    "type": "close.channel",
                    "text": message,
                })
            if data.get('hosts', None) and data.get('playbook', None) and data.get('playbook_name', None):
                hosts = get_hosts(data['hosts'])
                if not hosts:
                    self.message['status'] = 1
                    self.message['message'] = '未找到主机'
                    message = json.dumps(self.message)
                    async_to_sync(self.channel_layer.group_send)(self.group, {
                        "type": "close.channel",
                        "text": message,
                    })

                ansible_hosts = list()
                for host in hosts:
                    hostinfo = dict()
                    hostinfo['id'] = host.id
                    hostinfo['hostname'] = host.hostname
                    hostinfo['ip'] = host.ip
                    hostinfo['port'] = host.port
                    hostinfo['username'] = host.remote_user.username
                    hostinfo['password'] = host.remote_user.password
                    user = UserProfile.objects.get(username=self.scope.get('username'))
                    hostinfo['groups'] = [x.group_name for x in host.host_group.filter(user=user)]
                    if host.remote_user.enabled:
                        hostinfo['superusername'] = host.remote_user.superuser
                        hostinfo['superpassword'] = host.remote_user.superpass
                    else:
                        hostinfo['superusername'] = None
                    ansible_hosts.append(hostinfo)
                Run_playbook.delay(
                    hosts=ansible_hosts, group=self.group,
                    data=data,
                    user=self.scope.get('username'),
                    user_agent=self.user_agent,
                    client=self.client,

                )  # 执行
            else:
                self.message['status'] = 1
                self.message['message'] = '提交的数据格式错误'
                message = json.dumps(self.message)
                async_to_sync(self.channel_layer.group_send)(self.group, {
                    "type": "close.channel",
                    "text": message,
                })

    def send_message(self, data):
        try:
            self.send(data['text'])
        except Exception:
            print(traceback.format_exc())

    def close_channel(self, data):
        try:
            self.send(data['text'])
            time.sleep(0.3)
            self.close()
        except Exception:
            print(traceback.format_exc())

class Module(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = 'session_' + gen_rand_char()
        self.message = dict()
        self.client = None
        self.user_agent = None
        self.is_running = False

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(self.group, self.channel_name)  # 加入组
        for i in self.scope['headers']:
            if i[0].decode('utf-8') == 'user-agent':
                self.user_agent = i[1].decode('utf-8')
                break
        for i in self.scope['headers']:
            if i[0].decode('utf-8') == 'x-real-ip':
                self.client = i[1].decode('utf-8')
                break
            if i[0].decode('utf-8') == 'x-forwarded-for':
                self.client = i[1].decode('utf-8').split(',')[0]
                break
            self.client = self.scope['client'][0]

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(self.group, self.channel_name)  # 退出组
        except Exception:
            print(traceback.format_exc())

    def receive(self, text_data=None, bytes_data=None):
        if self.is_running:
            self.message['status'] = 1
            self.message['message'] = '当前通道已有任务在执行'
            message = json.dumps(self.message)
            async_to_sync(self.channel_layer.group_send)(self.group, {
                "type": "send.message",
                "text": message,
            })
        else:
            self.is_running = True
            data = dict()
            try:
                data = json.loads(text_data)
            except Exception:
                self.message['status'] = 1
                self.message['message'] = '提交的数据格式错误'
                message = json.dumps(self.message)
                async_to_sync(self.channel_layer.group_send)(self.group, {
                    "type": "close.channel",
                    "text": message,
                })
            if data.get('hosts', None) and data.get('module', None):
                hosts = get_hosts(data['hosts'])
                if not hosts:
                    self.message['status'] = 1
                    self.message['message'] = '未找到主机'
                    message = json.dumps(self.message)
                    async_to_sync(self.channel_layer.group_send)(self.group, {
                        "type": "close.channel",
                        "text": message,
                    })

                ansible_hosts = list()
                for host in hosts:
                    hostinfo = dict()
                    hostinfo['id'] = host.id
                    hostinfo['hostname'] = host.hostname
                    hostinfo['ip'] = host.ip
                    hostinfo['port'] = host.port
                    hostinfo['username'] = host.remote_user.username
                    hostinfo['password'] = host.remote_user.password
                    if host.remote_user.enabled:
                        hostinfo['superusername'] = host.remote_user.superuser
                        hostinfo['superpassword'] = host.remote_user.superpass
                    else:
                        hostinfo['superusername'] = None
                    ansible_hosts.append(hostinfo)
                Run_module.delay(
                    hosts=ansible_hosts, group=self.group,
                    data=data,
                    user=self.scope.get('username'),
                    user_agent=self.user_agent,
                    client=self.client,

                )  # 执行
            else:
                self.message['status'] = 1
                self.message['message'] = '提交的数据格式错误'
                message = json.dumps(self.message)
                async_to_sync(self.channel_layer.group_send)(self.group, {
                    "type": "close.channel",
                    "text": message,
                })

    def send_message(self, data):
        try:
            self.send(data['text'])
        except Exception:
            print(traceback.format_exc())

    def close_channel(self, data):
        try:
            self.send(data['text'])
            time.sleep(0.3)
            self.close()
        except Exception:
            print(traceback.format_exc())
