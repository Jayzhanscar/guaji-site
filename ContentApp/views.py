# -*- coding: utf-8 -*-
from django.shortcuts import render
from ContentApp.models import SmallText, Blog, Expert
from django.http import HttpResponse
from conf.common import USER_SUCCEED, TYPEERROR
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from ContentApp.models import Remark, AttentionTable
from django.http import *
from model.user.login import UserInfo
from common.mongohelper import get_db
import logging
import ContentApp.signals
# Create your views here.


# 导航中短词的搜索 // 根据key去搜索

@csrf_exempt
def index_nav(request):
    strin = []
    try:
        back_data = SmallText.objects.all()
        for i in back_data:
            strin.append(i.contentKey)
        return HttpResponse(str)
    except Exception as e:
        print(e)


# 获取机器学习介绍
@csrf_exempt
def introduce(request):
    return render(request, 'content/introduce.html')


# 用户发表文章
@csrf_exempt
def user_publish(request):
    if request.method == "POST":
        author = request.POST.get('user_id', None)
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        itype = request.POST.get('type', None)
        if author and author != 'undefined':
            if title:
                if content:
                    if type:
                        try:
                            if author:
                                author_id = request.COOKIES.get('UID')
                                User = UserInfo.objects.get(id=author_id)
                                user_blog = Blog()
                                user_blog.author = author
                                user_blog.title = str(title)
                                user_blog.tagline = str(content)
                                user_blog.type = itype
                                user_blog.user = User
                                user_blog.save()
                            return HttpResponse(USER_SUCCEED)
                        except Exception as e:
                            return HttpResponse(e)
                    return HttpResponse('not fond type')
                return HttpResponse('not fond content')
            return HttpResponse('not fond title')
        return HttpResponse('not fond author')
    else:
        return HttpResponse(TYPEERROR)


# 用户获取文章
@csrf_exempt
def blog_query(request):
    if request.method == "POST":
        sum_data = []
        user = request.POST.get('user_id')
        print(user)
        # 把数据序列化输出
        back_data = serializers.serialize('json', Blog.objects.filter(author=user))
    return HttpResponse(back_data, content_type="application/json")


# 分页获取文章数量
@csrf_exempt
def get_article(request):
    author = request.POST.get('user_id')
    page = request.POST.get('page')
    contact_list = Blog.objects.filter(author=author)
    for i in contact_list:
        print(i.title)
    paginator = Paginator(contact_list, 3)  # Show 3contacts per page
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
        print(contacts)
    print(contacts)
    return HttpResponse(contacts)


@csrf_exempt
def upload_img(request):
    if request.method == 'POST':
        file_img = request.POST.get('image')
        if file_img:
            back_data = {'data': 'ok'}
            return HttpResponse(back_data, content_type="application/json")


@csrf_exempt
def pull_article_page(request, article_id):
    """
    用户评论文章
    :param request: 
    :param article_id: 
    :return: 
    """
    userid = request.COOKIES.get('user_id')
    if request.method == "POST":
        content = request.POST.get('content')
        if userid and content:
            obj = UserInfo.objects.filter(Account=userid)
            obj1 = Blog.objects.filter(id=article_id)
            for i in obj:
                for j in obj1:
                    myremark = Remark()
                    myremark.speaker = i
                    myremark.article = j
                    myremark.message = content
                    myremark.save()
                    sum_count = Remark.objects.filter(article_id=article_id).count()
                    blog = Blog.objects.get(id=article_id)
                    blog.talk_count = sum_count
                    blog.save()
            # 监听评论消息并且发送给文章用户

        else:
            return HttpResponseRedirect('/user/login/')
    count = Blog.objects.get(id=article_id)
    # 增加浏览量
    count.increase_views()
    userid = request.COOKIES.get('user_id')
    if not userid:
        return HttpResponseRedirect('/user/relogin/')
    p = UserInfo.objects.filter(Account=userid)
    img_name = ''
    is_focus = 0
    for i in p:
        img_name = i.img.url
    tags = Blog.objects.filter(id=article_id)
    for i in tags:
        count1 = UserInfo.objects.filter(id=i.user_id)
        obj = AttentionTable.objects.filter(Concern=userid, Concerned=count1)
        if obj:
            is_focus = 1
    ctx = {
        'ties': Remark.objects.filter(article_id=article_id),
        'tag': Blog.objects.filter(id=article_id),
        'articles_id': article_id,
        'imgs': p,
        'img_name': img_name,
        'p': p,
        'is_focus': is_focus
    }
    return render(request, 'content/article_detail.html', ctx)


@csrf_exempt
def click_like(request):
    """
    点赞处理(附加统计文章评论数--celery)
    :param request: 
    :return: 
    """
    if request.method == 'POST':
        article_id = request.POST.get('art_id')
        if article_id:
            try:
                talk_count = Remark.objects.filter(id=article_id).count()
                art = Blog.objects.get(id=article_id)
                art.increase_like()
                art.talk_count = talk_count
                art.save()
                data = {'code': 0}
                return JsonResponse(data)
            except Exception as e:
                print(e)
                return HttpResponse('error')
        else:
            return HttpResponse('no id')


@csrf_exempt
def setting(request):
    """
    用户信息设置页面
    :param request: 
    :return: 
    """
    user = request.COOKIES["user_id"]
    if request.method == 'POST':
        action = request.POST.get('action')
        File = request.FILES.get('file')
        if action == 'upload' and File:
            try:
                User = UserInfo.objects.get(Account=user)
                User.img = File
                User.save()
                return HttpResponse('1')
            except Exception as e:
                print(e)
                return HttpResponse('0')
        if action == 'save':
            username = request.POST.get('name')
            useremail = request.POST.get('email')
            usersex = request.POST.get('sex')
            userjianjie = request.POST.get('jianjie')
            if username:
                if useremail:
                    if usersex:
                        if userjianjie:
                            print(username, usersex, useremail, userjianjie)
                            U = UserInfo.objects.get(Account=user)
                            U.userName = username
                            U.jianjie = userjianjie
                            U.userEmail = useremail
                            U.sex = usersex
                            U.save()
                            return HttpResponse('ok')
                        return HttpResponse('no jianjie')
                    return HttpResponse('no sex')
                return HttpResponse('no usermail')
            return HttpResponse('no username')
    if user:
        p = UserInfo.objects.filter(Account=user)
    return render(request, 'content/setting.html', locals())


@csrf_exempt
def iframe_article(request):
    """
    用户信息设置页面
    :param request: 
    :return: 
    """
    user_id = request.COOKIES.get('user_id')
    try:
        max = 0
        search_content = ''
        db = get_db()
        b = db.gg_search.find({'user': user_id})
        for j in b:
            if max < j['create_time']:
                max = j['create_time']
                search_content = j['content']
        user_obj = UserInfo.objects.filter(userName__contains=search_content)[0:3]
        if not user_obj:
            user_obj = UserInfo.objects.all()[0:3]
        wz = Blog.objects.filter(title__contains=search_content)
        count = wz.count()
    except Exception as e:
        print(e)
    return render(request, 'content/luntan/article.html', locals())


@csrf_exempt
def expert(request):
    """
    专家总浏览页面
    :param request: 
    :return: 
    """
    user_id = request.COOKIES.get('user_id')
    if user_id:
        p = UserInfo.objects.filter(Account=user_id)
    experts = Expert.objects.all()
    return render(request, 'content/expert/expert.html', locals())


@csrf_exempt
def expert_detail(request, expert_id):
    """
         :param request: 
         :param expert_id: 专家详情页
         :return: 
         """
    user_id = request.COOKIES.get('user_id')
    if user_id:
        p = UserInfo.objects.filter(Account=user_id)
    experts = Expert.objects.filter(id=expert_id)
    return render(request, 'content/expert/expert_detail.html', locals())
