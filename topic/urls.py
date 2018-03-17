# -*- coding: utf-8 -*-
from django.conf.urls import url
from topic import views
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^default$', views.default),
    url(r'^default/(?P<topic_id>\w+)$', views.topic_detail),
]