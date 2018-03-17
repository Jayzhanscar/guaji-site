# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import MySQLdb as mdb
# Create your tests here.

conn = mdb.connect(host='101.132.187.204', port=3306, user='root', passwd='root', db='bysj', charset='utf8')
print(conn)
