# -*- coding: utf-8 -*-
from django.conf.urls import url
from ContentApp import views
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^index_pav/$', views.index_nav),
    # 发表页面获取
    url(r'^introduce/$', views.introduce),
    # 文章发布
    url(r'^user_publish/$', views.user_publish),
    # 文章查询
    url(r'^blog_query/$', views.blog_query),
    # 分页文章获取
    url(r'^get_article/$', views.get_article),
    # 文章详情页
    url(r'^pull_article.page/(?P<article_id>\w+)$', views.pull_article_page),
    # 接收上传的图片
    url(r'^upload_img/$', views.upload_img),
    # 评论功能
    # 点赞(顺便统计评论参数)
    url(r'^like/$', views.click_like),
    # 用户设置
    url(r'^setting$', views.setting),
    # iframe 文章
    url(r'^iframe_article$', views.iframe_article),
    # 专家页面
    url(r'^expert$', views.expert),
    # 专家详情页
    url(r'^expert_detail/(?P<expert_id>\w+)$', views.expert_detail)
]