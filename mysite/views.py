from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .form import Loginform, Registerform
from django.urls import reverse
# Create your views here.


def home(requests):
    context = {}
    context['hello'] = '欢迎光临我的博客'
    return render(requests, 'home.html', context)


def login(requests):
    if requests.method == "POST":
        login_form = Loginform(requests.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(requests, user)
            return redirect(requests.GET.get('from', reverse('home')))
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
            return redirect(requests.GET.get('from', reverse('home')))
    else:
        register_form = Registerform()
    context = {}
    context['register_form'] = register_form
    return render(requests, 'register.html', context)
