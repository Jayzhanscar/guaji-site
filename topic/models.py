# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models

# Create your models here.


class Topic(models.Model):
    """
    专题目录表
    """
    # 专题id
    topic_id = models.IntegerField(primary_key=True, db_column='topic_id')
    # 专题名字
    topic_name = models.CharField(max_length=50)
    # 专题描述
    topic_drc = models.CharField(max_length=150)
    # 专题创建者
    topic_author = models.CharField(max_length=20)
    #  头像路径
    img = models.ImageField(upload_to='img', default='null')
    # 文章数目
    topic_article = models.IntegerField()
    # 关注人数
    topic_focus = models.IntegerField()
    # 专题公告
    topic_notice = models.CharField(max_length=300, default='null')
    # 创建时间
    create_date = models.DateTimeField(default=datetime.datetime.utcnow, db_column='topic_create_date')

    def increase_article(self):
        """
        浏览量
        :return: 
        """
        self.topic_article += 1
        self.save(update_fields=['topic_article'])

    class Meta:
        app_label = 'Topic'
        db_table = "topic"