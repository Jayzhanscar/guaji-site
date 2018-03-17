# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from model.user.login import UserInfo
from common.mongohelper import get_db
from ContentApp.models import Blog
from django.core import serializers
from django.shortcuts import render
from topic.models import Topic
# Create your views here.


def default(request):
    re = request.COOKIES.get('user_id')
    if re:
        p = UserInfo.objects.filter(Account=re)
    obj = Topic.objects.all()
    return render(request, 'topic/index.html', locals())


def topic_detail(request, topic_id):
    """
     :param request: 
     :param topic: 
     :return: 
    """

    user_id = request.COOKIES.get('user_id')
    if request.method == 'POST':
        acticon = request.POST.get('action')
        article_id = request.POST.get('article_id')
        print(acticon, article_id)
        Bobj = Blog.objects.get(id=article_id)
        if Bobj:
            print(Bobj)
            Bobj.topic_name = topic_id
            Bobj.save()
            return HttpResponse('ok')
    if user_id:
        p = UserInfo.objects.filter(Account=user_id)
        wz = Blog.objects.filter(author=user_id)[0:7]
    try:
        obj = Topic.objects.filter(topic_id=topic_id)
        topic_articles = Blog.objects.filter(topic_name=topic_id)
    except Exception as e:
        print(e)
    return render(request, 'topic/topic_detail.html', locals())