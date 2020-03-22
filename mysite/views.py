from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib import auth
from .form import Loginform
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