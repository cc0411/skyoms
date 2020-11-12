from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.http import JsonResponse
from django.http import HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from users.utils import get_cookie
from users.utils import get_captcha
from users.utils import get_user_menu
from users.utils import get_user_router
from users.exceptions import *
from django.core.cache import cache
from io import BytesIO
from skyoms.expiring_token_authentication import ExpireTokenAuthentication
from rest_framework import permissions
from rest_framework.views import APIView
from django.views import View
from .models import LoginRecord
from utils.BaseViews import BaseView
from .serializers import LoginRecordSerializer
import json
import uuid
import datetime

# Create your views here.
from django.contrib.auth import get_user_model
User = get_user_model()

#重写自定义登陆认证方式，使用邮箱和用户名
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return  user
        except Exception as e:
            return None

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        result = {
            'code': 0,
            'msg': '登录成功',
            'data': {
                'username': '',
                'password': '',
                'name': '',
                'token': '',
                'uuid': '',
                'menu': '',
                'router': ''
            }
        }
        try:
            login_ip = request.META['REMOTE_ADDR']
            raw_data = json.loads(request.body.decode('utf-8'))
            username = raw_data.get('username')
            password = raw_data.get('password')
            captcha = raw_data.get('code').lower()
            image_uuid = raw_data.get('image_uuid')
            # 判断验证码
            captcha_redis = cache.get(image_uuid)
            if not captcha_redis:
                raise CaptchaError('验证码过期')
            else:
                captcha_redis = captcha_redis.lower()
            if captcha_redis != captcha:
                raise CaptchaError('验证码错误')
            # 验证账号密码
            user = authenticate(username=username, password=password)
            if user:
                # 随机token
                rand_token = get_cookie(username)
                # 更新django登录状态
                login(request, user)
                # 保存最新token到数据库
                token_obj = Token.objects.filter(user=user)

                if token_obj:
                    token_obj.update(**{'key': rand_token, 'created': datetime.datetime.now()})
                else:
                    Token.objects.create(user=user, key=rand_token)
                # 获取登录用户有权限访问的菜单和路由
                menu = get_user_menu(user)
                router = get_user_router(user)
                # 插入审计日志
                LoginRecord.objects.create(user=request.user,ip=login_ip,login_time=datetime.datetime.now())
                data = {
                    'username': username,
                    'name': username,
                    'token': rand_token,
                    'uuid': str(uuid.uuid4()),
                    'menu': menu,
                    'router': router
                }
                result['data'] = data
            else:
                result = {
                    'code': 401,
                    'msg': '用户名或密码错误',
                    'data': {}
                }
        except CaptchaError as e:
            result = {
                'code': 402,
                'msg': str(e),
                'data': {}
            }
        except Exception as e:
            result = {
                'code': 500,
                'msg': str(e),
                'data': {}
            }
        finally:
            return JsonResponse(result)

@csrf_exempt
def user_captcha(request, image_uuid):
    if request.method == 'GET':
        try:
            chars, image = get_captcha()
            cache.set(image_uuid, chars, timeout=180)
            bf = BytesIO()
            image.save(bf, 'png')
            bf.getvalue()
        except Exception as e:
            print(str(e))
        return HttpResponse(bf.getvalue(), content_type='image/png')

class ListUserMenu(APIView):
    """用户有权限访问的菜单数据"""
    authentication_classes = (ExpireTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        result = {
            'code': 0,
            'msg': '请求成功',
            'data': {
                'menu': '',
            }
        }
        try:
            user = request.user
            menu = get_user_menu(user)
            result['data']['menu'] = menu

        except Exception as e:
            result = {
                'code': 500,
                'msg': str(e),
                'data': {}
            }
        finally:
            return JsonResponse(result)

class ListUserRouter(APIView):
    """用户有权限访问的路由数据"""
    authentication_classes = (ExpireTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        result = {
            'code': 0,
            'msg': '请求成功',
            'data': {
                'router': '',
            }
        }
        try:
            user = request.user
            router = get_user_router(user)
            result['data']['router'] = router

        except Exception as e:
            result = {
                'code': 500,
                'msg': str(e),
                'data': {}
            }
        finally:
            return JsonResponse(result)

class LoginRecordViewSet(BaseView):
    queryset = LoginRecord.objects.all().order_by("-login_time")
    serializer_class = LoginRecordSerializer

