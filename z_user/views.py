# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from model.user.login import UserInfo
from hashlib import sha1
from django.template.loader import get_template
from django.template import Context
import json
from django.shortcuts import render, redirect, HttpResponseRedirect, render_to_response
from ContentApp.models import Blog
# 导入缓存数据
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from conf import common
from ContentApp.models import Blog, Expert, Remark, AttentionTable
from django.utils.encoding import smart_str
# from conf.get_name import write_to_cache, read_from_cache
from django.contrib.auth import authenticate,login,logout
import urllib.parse


@csrf_exempt
def relogin(request):
    return render(request, 'user/login.html', )


@csrf_exempt
def info(request):
    userid = request.COOKIES.get('user_id')
    p = UserInfo.objects.filter(Account=userid)
    articles = Blog.objects.all().order_by('-views')[0:15]
    experts = Expert.objects.all()[0:5]
    return render(request, 'user/index.html', locals())
# 注册账号时采用post请求


# 发表页面
@csrf_exempt
def publish(request):
    user = request.COOKIES["user_id"]
    if user:
        try:
            count = Blog.objects.filter(author=user).count()
            p = UserInfo.objects.filter(Account=user)
        except:
            print('获取失败')

    return render(request,'content/publish.html',locals())


# 用户中心
@csrf_exempt
def user_center(request):
    userid = request.COOKIES.get('user_id')
    if request.method == 'POST':
        try:
            my_img = UserInfo.objects.get(Account=userid)
            my_img.img = request.FILES.get('img')
            my_img.imgname = request.FILES.get('img').name
            my_img.save()
        except Exception as e:
            print('保存错误', e)
        return render(request, 'user/usercenter.html')
    p = UserInfo.objects.filter(Account=userid)
    for i in p:
        img_name = i.img.url
    if userid:
        articles = Blog.objects.filter(author=userid)
        obj1 = AttentionTable.objects.filter(Concern=userid)
        print(obj1)
        for i in obj1:
            print(i)
    if not userid:
        return HttpResponseRedirect('/user/relogin')
    return render(request, 'user/usercenter.html', locals())


@csrf_exempt
def register(request):
    username = request.POST.get('name')
    userpwd = request.POST.get('pwd')
    userpwd1 = request.POST.get('pwd1')
    useremail = request.POST.get('email')
    # 判断两次密码
    if userpwd != userpwd1:
        return HttpResponse(common.USER_ATPISM)
    # 判断用户名是否重复
    else:
        try:
            users = UserInfo.objects.filter(userName=username)
            if users:
                return HttpResponse(common.USER_EXITS)
            else:
                s1 = sha1()
                s1.update(userpwd.encode("utf8"))
                upwd2 = s1.hexdigest()
                # 创建数据表对象
                # 创建对象
                user = UserInfo()
                user.userName = username
                user.userPwd = upwd2
                user.Account = useremail
                user.save()
                return HttpResponse(common.USER_SUCCEED)
        except Exception as e:
            print(e)


# 验证账号 post请求
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        userpwd = request.POST.get('pwd')
        try:
            users_name = UserInfo.objects.filter(Account=username)
        except Exception as e:
            print(e)
        if users_name:
            s1 = sha1()
            s1.update(userpwd.encode("utf8"))
            if s1.hexdigest() == users_name[0].userPwd:
                User = UserInfo.objects.get(Account=username)
                resp = {'data': 1}
                response = HttpResponse(json.dumps(resp), content_type="application/json")
                response.set_cookie('user_id', User.Account, 36000)
                # cooike 保存用户ID
                response.set_cookie('UID', User.id, 36000)
                # 把用户名写到redis缓存里面去
                # write_to_cache(username)
                return response
            else:
                back_data = {'data': 'no user'}
                return HttpResponse(back_data, content_type="application/json")
        else:
            back_data = {'data': 'request faild'}
            return HttpResponse(back_data, content_type="application/json")


# 修改用户信息
@csrf_exempt
def edit_user(request):
    if request.method == "POST":
        userid = request.POST.get('user_id')
        user_name = request.POST.get('name')
        qianm = request.POST.get('qianming')
        qq = request.POST.get('qq')
        if user_name:
            try:
                u = UserInfo.objects.get(userName=userid)
                u.userName = user_name
                u.qianming = qianm
                u.qq = qq
                u.save()
                response = HttpResponse(user_name)
                response.set_cookie('user_id', user_name)
                return response
            except:
                print('保存错误')
                return HttpResponse('error')
        else:
            return HttpResponse('no name')
