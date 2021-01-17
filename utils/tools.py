# -*- coding:utf-8 -*-
import random
from rest_framework.authentication import SessionAuthentication
import sys
import ipaddress
import socket

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

class BaseResponse(object):

    def __init__(self):
        self.code = 200
        self.data = None
        self.error = None

    @property
    def dict(self):
        return self.__dict__






class LegalIP(object):
    def __init__(self,ip):
        self.ip = ip
        self.data = {}

    def get_host_ip(self):
        """
        查询本机ip地址
        :return: ip
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('192.168.1.1', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
            return ip

    def valid_ip(self):
        """
        验证ip是否有效,比如192.168.1.256是一个不存在的ip
        :return: bool
        """
        try:
            # 判断 python 版本
            if sys.version_info[0] == 2:
                ipaddress.ip_address(self.ip.strip().decode("utf-8"))
            elif sys.version_info[0] == 3:
                # ipaddress.ip_address(bytes(ip.strip().encode("utf-8")))
                ipaddress.ip_address(self.ip)

            return True
        except Exception as e:
            print(e)
            return False

    def check_tcp(self, port=22, timeout=1):
        """
        检测tcp端口,这里主要是检测ssh端口是否开放
        :param ip: ip地址
        :param port: 端口号
        :param timeout: 超时时间
        :return: bool
        """
        flag = False
        try:
            socket.setdefaulttimeout(timeout)  # 整个socket层设置超时时间
            cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            address = (str(self.ip), int(port))
            status = cs.connect_ex((address))  # 开始连接
            cs.settimeout(timeout)

            if not status:
                flag = True

            return flag
        except Exception as e:
            print("error:%s" % e)
            return flag

    def test_parameter(self):
        """
        判断网页传递的ip是否合法
        :return: bool
        """
        if self.ip == self.get_host_ip():
            self.data['error'] = "ip不能是本服务器"
            return self.data

        if not self.valid_ip():
            self.data['error'] = "ip地址不合法"
            return self.data

        if not self.check_tcp():
            self.data['error'] = "ssh端口不可达"
            return self.data

def gen_rand_char(length=16, chars='0123456789zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA'):
    return ''.join(random.sample(chars, length))