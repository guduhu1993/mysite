from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .form import Loginform, Registerform, UpdateEmail
from django.urls import reverse
import datetime
import jwt
from jwt import exceptions
# Create your views here.


def home(requests):
    context = {}
    context['hello'] = '欢迎光临我的博客'
    return render(requests, 'home.html', context)

SALT='sadffffffffpp0'
def create_token():
    # 构造headers
    headers = {'typ': 'jwt', 'alg': 'HS256'}
    # 构造payload
    payload = {
        'user_id': 1, # 自定义用户ID
        'username': 'wupeiqi', # 自定义用户名
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=3000) # 超时时间
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
            result=create_token()
            print(requests.GET.get('from'))
            response=redirect(requests.GET.get('from', reverse('home')))
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
            result=create_token()
            response = redirect(requests.GET.get('from', reverse('home')))
            response.set_cookie('jwt_token', result, max_age=10000)
            return response
    else:
        register_form = Registerform()
    context = {}
    context['register_form'] = register_form
    return render(requests, 'register.html', context)


def logout(requests):
    auth.logout(requests)
    return redirect(requests.GET.get('from', reverse('home')))


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
