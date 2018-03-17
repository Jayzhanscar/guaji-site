# -*- coding: utf-8 -*-
from django.conf.urls import url
from api import views

urlpatterns = [
    # 搜索内容保存到mongo中，路由跳转至搜索展示页面
    url(r'^search_home$', views.search_home),
    # 关注作者
     url(r'^focus_people$', views.focus_people),
    ]
