from django import forms
from django.contrib import auth
# from django.contrib.auth.models import User
from users.models import User


class Loginform(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(
        attrs={"class": "form-control", "placehoder": "Default input"}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={"class": "form-control", "placehoder": "密码"}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class Registerform(forms.Form):
    username = forms.CharField(label='用户名', max_length=30, min_length=3, required=True, widget=forms.TextInput(
        attrs={"class": "form-control", "placehoder": "请输入用户名"}))
    mobile = forms.CharField(label='用户名', max_length=11, min_length=11, required=True, widget=forms.TextInput(
        attrs={"class": "form-control", "placehoder": "请输入手机号"}))
    verify_pic = forms.CharField(label='用户名', max_length=30, min_length=3, required=True, widget=forms.TextInput(
        attrs={"class": "form-control", "placehoder": "输入验证码", "onchange": "verify_code(this);"}))
    email = forms.EmailField(
        label='邮箱', max_length=30, min_length=3,
        widget=forms.EmailInput(attrs={"class": "form-control", "placehoder": "请输入邮箱"}))
    password = forms.CharField(
        label='密码', max_length=30, min_length=3,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placehoder": "请输入密码"}))
    password_again = forms.CharField(
        label='密码', max_length=30, min_length=3,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placehoder": "请再输入一次密码"}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已存在")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已存在")
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password_again != password:
            raise forms.ValidationError("密码不一致")
        return password_again


class UpdateEmail(forms.Form):
    email = forms.EmailField(label='邮箱', required=True, widget=forms.EmailInput(
        attrs={"class": "form-control", "placehoder": "请输入邮箱"}))

    def __init__(self, *args, **kwargs):
        if "user" in kwargs:
            self.user = kwargs.pop('user')
        super(UpdateEmail, self).__init__(*args, **kwargs)

    def clean_email(self):
        print(self.user)
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已存在")
        return email
