# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
import datetime
from django.contrib import admin
from django.db import models
from django import forms
from celery_app.mail import send_email
from ContentApp import signals
from model.user.login import UserInfo
from django.db.models.signals import pre_save
import logging
from celery_app.mail import send_email
# Create your models here.

TOPIC_CHOICES = (
  ('level1', 'Bad'),
  ('level2', 'SoSo'),
  ('level3', 'Good'),
)


class SmallText(models.Model):

    """
    存储一些页面上带有key的文本（短）
    """
    # key
    typeKey = models.CharField(max_length=20)
    # content
    contentKey = models.CharField(max_length=40)
    # 添加时间
    create_date = models.DateTimeField(default=datetime.datetime.utcnow, db_column='ebf_html_create_date')
    # 更改时间
    update_date = models.DateTimeField(default=datetime.datetime.utcnow, db_column='ebf_html_update_date')

    class Meta:
        app_label = 'ContentApp'
        db_table = "ml_small_text"



class LongText(models.Model):
    """
    用来存储文本信息
    """
    """
       存储一些页面上带有key的文本（短）
       """
    # key
    Title = models.CharField(max_length=20)
    # content
    Content = models.TextField()
    # 添加时间
    create_date = models.DateTimeField(default=datetime.datetime.now, db_column='ebf_html_create_date')
    # 更改时间
    update_date = models.DateTimeField(default=datetime.datetime.now, db_column='ebf_html_update_date')

    class Meta:
        app_label = 'ContentApp'
        db_table = "ml_long_text"


class Blog(models.Model):
    """
    存入发表的文章
    """
    # 文章id
    id = models.IntegerField(db_column='blog_id', primary_key=True)
    # 存入作者
    author = models.CharField(max_length=20)
    # 用户信息表
    user = models.ForeignKey(UserInfo, null=True, on_delete=models.SET_NULL)
    # 文章标题
    title = models.CharField(max_length=100)
    # 文章正文
    tagline = models.TextField()
    # 文章类别
    type = models.CharField(max_length=20)
    # 文章浏览量
    views = models.PositiveIntegerField(default=0)
    # 文章评论数量
    talk_count = models.IntegerField(default=0)
    # 文章点赞数
    like_count = models.PositiveIntegerField(default=0)
    # 专题 默认为空
    topic_name = models.CharField(max_length=50, default='null')
    # 添加时间
    create_date = models.DateTimeField(default= timezone.now, db_column='ebf_html_create_date')

    class Meta:
        app_label = 'ContentApp'
        db_table = "blog"

    def increase_views(self):
        """
        浏览量
        :return: 
        """
        self.views += 1
        self.save(update_fields=['views'])

    def increase_like(self):
        """
        点赞量
        :return: 
        """
        self.like_count += 1
        self.save(update_fields=['like_count'])


class Comment(models.Model):
    # id
    id = models.IntegerField(primary_key=True, default=1, db_column='commit_id')
    # 文章标签
    article_id = models.ForeignKey(Blog, db_column='article_id', on_delete=models.CASCADE, default=1)
    # 点赞/评论
    action = models.CharField(max_length=10, db_column='art_action', default=None)
    # 评论者名称
    name = models.CharField(max_length=100)
    # 评论内容
    text = models.TextField()
    # 评论时间
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'ContentApp'
        db_table = "comment"


class RemarkForm(forms.Form):
    """
    评论表单 -----  todo 已作废
    """
    speaker = models.CharField(max_length=50)
    author = models.CharField(max_length=30)
    title = models.CharField(max_length=50)
    message = models.CharField(max_length=300)


class Remark(models.Model):
    """
    文章评论表单
    """
    # id
    id = models.IntegerField(primary_key=True)
    # 评论者
    speaker = models.ForeignKey(UserInfo, null=True, on_delete=models.SET_NULL)
    # 作者
    article = models.ForeignKey(Blog, null=True, on_delete=models.SET_NULL)
    # 评论内容
    message = models.CharField(max_length=300)
    # 评论时间
    create_date = models.DateTimeField(default=timezone.now, db_column='talk_create_date')

    class Meta:
        ordering = ['speaker_id']

# signals.comment_done.connect(Remark.zhutao, sender=Remark)


class AttentionTable(models.Model):
    """
    关注表单
    """
    id = models.IntegerField(primary_key=True)
    # 关注的人
    Concern = models.CharField(max_length=100)
    # 被关注的人
    Concerned = models.ForeignKey(UserInfo, null=True, on_delete=models.SET_NULL, related_name='concerned', verbose_name='2')
    # 关注的时间
    create_date = models.DateTimeField(default=timezone.now, db_column='concern_create_date')


class Expert(models.Model):
    """
    推荐专家表
    """
    id = models.IntegerField(primary_key=True, db_column='expert_id')
    # 姓名
    name = models.CharField(max_length=20, db_column='expert_name')
    # 头像
    img = models.CharField(max_length=50, db_column='expert_img')
    # 简介
    introduce = models.CharField(max_length=250, db_column='expert_introduce')
    # 创建时间
    create_date = models.DateTimeField(default=timezone.now, db_column='expert_create_date')


from django.db.models.signals import pre_save
from django.dispatch import receiver


# 收到评论 保存数据库之前提醒用户
@receiver(pre_save, sender=Remark)
def my_handler(sender, instance, **kwargs):
    """
    
    :param sender: 数据对象
    :param instance: 对象实例
    :param kwargs: 可以自行添加信息
    :return: 
    """
    content = '尊敬的用户您好，您写的文章收到一条回复'
    send_email('959370553@qq.com,zhanljscarever@163.com', 'D:\\test', content)