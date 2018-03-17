# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models

# Create your models here.


class UserInfo(models.Model):
    """
    用户信息表
    """
    id = models.IntegerField(db_column='user_id', primary_key=True)
    # 用户名
    userName = models.CharField(max_length=20)
    # 登录密码
    userPwd = models.CharField(max_length=40)
    # 邮箱
    userEmail = models.CharField(max_length=30)
    # 住址
    userAddress = models.CharField(max_length=100, default='')
    # 电话
    userTel = models.CharField(max_length=11, default='')
    # 登陆账号
    Account = models.IntegerField(default=0)
    # 头像地址
    img_path = models.CharField(max_length=100, default='/static/img/touxiang.jpg')
    # 个性签名
    qianming = models.CharField(max_length=100, default='')
    # 头像地址
    img = models.ImageField(upload_to='img', default='static/img/111.jpg')
    # 头像图片名字
    imgname = models.CharField(max_length=20, default='null')
    # 性别 1：男 2：女
    sex = models.IntegerField(default=0)
    # 个人简介
    jianjie = models.TextField(default='null')
    # 创建时间
    create_date = models.DateTimeField(default=datetime.datetime.utcnow, db_column='user_create_date')

    class Meta:
        app_label = 'z_user'
        db_table = "zw_user"
