# -*- coding: utf-8 -*-
from django.conf.urls import url
from show import views
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^index_1$', views.index_1),
    # 发表页面获取
    url(r'^index_3$', views.index_3),
    url(r'^index_2$', views.index_2),
    url(r'^process$', views.process),
    url(r'^transform$', views.transform),
    url(r'^chat$', views.chat),



]