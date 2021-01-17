from django.test import TestCase
import redis
# Create your tests here.
from utils.Ansible_api import AnsibleAPI
from utils.callback import SetupCallbackModule,ModuleCallbackModule,CopyCallbackModule,PlayBookCallbackModule
from utils.inventory import BaseInventory

#conn = redis.Redis(host='localhost',port=6379,password='Redis@123')

host_data=[{'hostname': 'test1', 'ip': '192.168.57.3', 'port': 22, 'username': 'root', 'password': 'gAAAAABfyHVlwUdpH1HtXHInYsZWYafzlO6Ii6SquBDVGWeaCMwc-0JMPr7xDxzISOnD4Lgn9Mg8APqgmBVoG41yzJMnQoeRpA=='}]
inventory = BaseInventory(host_data)
callback = SetupCallbackModule()
ansible_api = AnsibleAPI(dynamic_inventory=inventory,callback=callback)



if __name__ =="__main__":
    server_info, failed, unreach, error = ansible_api.get_server_info(hosts='all')
    print(server_info)