from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib import auth
# from django.contrib.auth.models import User
from users.models import User
from .form import Loginform, Registerform, UpdateEmail
from django.urls import reverse
import datetime
import jwt
from jwt import exceptions
from .settings import SALT
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from mysite.gen_pic import GenPic
import json
# Create your views here.

def login_required(func):
    def wrapper(requests, *args, **kwargs):
        jwt_token = requests.COOKIES.get('jwt_token')
        result = parse_payload(jwt_token)
        if result['error']:
            return redirect('login')
        return func(requests, *args, **kwargs)
    return wrapper

def home(requests):
    context = {}
    context['hello'] = '欢迎光临我的博客'
    return render(requests, 'home.html', context)


def create_token(expire_time):
    # 构造headers
    headers = {'typ': 'jwt', 'alg': 'HS256'}
    # 构造payload
    payload = {
        'user_id': 1, # 自定义用户ID
        'username': 'wupeiqi', # 自定义用户名
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=expire_time) # 超时时间
    }
    result = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers).decode('utf-8')
    return result

def parse_payload(token):
    """
    对token进行和发行校验并获取payload
    :param token:
    :return:
    """
    result = {'status': False, 'data': None, 'error': None}
    try:
        verified_payload = jwt.decode(token, SALT, True)
        result['status'] = True
        result['data'] = verified_payload
    except exceptions.ExpiredSignatureError:
        result['error'] = 'token已失效'
    except jwt.DecodeError:
        result['error'] = 'token认证失败'
    except jwt.InvalidTokenError:
        result['error'] = '非法的token'
    return result

def login(requests):
    if requests.method == "POST":
        login_form = Loginform(requests.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(requests, user)
            result=create_token(2)
            print(requests.GET.get('from'))
            if not requests.GET.get('from') in ['/register/','/login/']:
                redirect_url = requests.GET.get('from', reverse('home'))
            else:
                redirect_url =  requests.GET.get('home', reverse('home'))
            response=redirect(redirect_url)
            response.set_cookie('jwt_token', result, max_age=10000)
            return response
    else:
        login_form = Loginform()
    context = {}
    context['login_form'] = login_form
    return render(requests, 'login.html', context)


def register(requests):
    if requests.method == "POST":
        register_form = Registerform(requests.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User.objects.create_user(
                username=username, email=email, password=password)
            user.save()
            # 登录
            user = auth.authenticate(username=username, password=password)
            auth.login(requests, user)
            result=create_token(2)
            if not requests.GET.get('from') in ['/register/','/login/']:
                redirect_url = requests.GET.get('from', reverse('home'))
            else:
                redirect_url =  requests.GET.get('home', reverse('home'))
            response=redirect(redirect_url)
            # response = redirect(requests.GET.get('from', reverse('home')))
            response.set_cookie('jwt_token', result, max_age=10000)
            return response
    else:
        register_form = Registerform()
    context = {}
    context['register_form'] = register_form
    return render(requests, 'register.html', context)


def logout(requests):
    auth.logout(requests)
    result=create_token(0)
    print(requests.GET.get('from'))
    response = redirect(requests.GET.get('from', reverse('home')))
    response.set_cookie('jwt_token', result, max_age=10000)
    return response


def user_info(requests):
    context = {}
    return render(requests, 'user_info.html', context)


def update_email(requests):
    if requests.method == "POST":
        email_form = UpdateEmail(requests.POST, user=requests.user)
        if email_form.is_valid():
            email = email_form.cleaned_data['email']
            user = requests.user
            user.email = email
            user.save()
            return redirect(requests.GET.get('from', reverse('home')))
    else:
        email_form = UpdateEmail()
    context = {}
    context['email_form'] = email_form
    return render(requests, 'update_email.html', context)


def post(self, requests):
    user_name = requests.GET.get('username')
    password = requests.GET.get('password')
    token_payload = {}
    login_form = Loginform(requests.POST)
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        password = login_form.cleaned_data['password']
        # 构造header
        token_header = {'alg':'HS256', 'typ':"jwt"}
        # 构造payload
        token_payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
        token = jwt.encode(headers=token_header, payload=token_payload, key=SALT, algorithm='HS256').decode('utf-8')

class ImageCodeView(APIView):
    """
    图片验证码
    """
    def get(self, request, pic_id):
        """
        获取图片验证码
        """
        print(pic_id)
        # 生成验证码图片
        genpic = GenPic()
        text, image = genpic.gene_code(request)
        # 固定返回验证码图片数据，不需要REST framework框架的Response帮助我们决定返回响应数据的格式
        # 所以此处直接使用Django原生的HttpResponse即可
        print(text.lower())
        with open("dictionary.json","r") as f:
            pic_dic = json.loads(f.read())
            pic_dic[pic_id] = text.lower()
        with open("dictionary.json","w") as f:
            f.write(json.dumps(pic_dic))
        return HttpResponse(image, content_type="images/png")

class VerifyPic(APIView):
    # 验证手机号规范、用户名规范是否已存在、验证码正确性、邮箱规范是否已存在
    def post(self,request,pic_id):
        data = {}
        print('------',pic_id)
        print('======',request.POST.get('pic_str'))
        with open("dictionary.json","r") as f:
            pic_code_dic = json.loads(f.read())
            # print('******',pic_code_dic)
            # print('+++++++',pic_code_dic[str(pic_id)])
        if pic_code_dic[str(pic_id)] == request.POST.get('pic_str').lower():
            data['status'] = 'SUCCESS'
        else:
            data['status'] = 'ERROR'
        return JsonResponse(data)
    