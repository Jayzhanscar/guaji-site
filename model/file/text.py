# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models

# Create your models here.


class FileText(models.Model):
    """
     文本文件 
    """
    # 文件名字
    fileName = models.CharField(max_length=20)
    # 文件内容
    fileContent = models.TextField()
    # 创建时间
    create_date = models.DateTimeField(default=datetime.datetime.utcnow, db_column='ebf_html_create_date')

    def __str__(self):
        return self.fileName

    class Meta:
        app_label = 'z_user'
        db_table = "zw_wj"


# 建立视频文件 todo ...

# 建立图片文件 todo ...






