from django.contrib import admin
from ContentApp.models import SmallText, Blog, LongText, Remark
from model.user.login import UserInfo
# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'views', 'type', 'talk_count', 'create_date')

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('create_date',)

    # fk_fields 设置显示外键字段
    fk_fields = ('user',)

    # list_editable 设置默认可编辑字段
    # list_editable = ['title']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'title')

    list_filter = ('title', 'author')  # 过滤器
    search_fields = ('title', 'author', 'create_date')  # 搜索字段
    # date_hierarchy = 'create_date'  # 详细时间分层筛选　


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'userName', 'Account', 'img', 'create_date')

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('create_date',)

    # fk_fields 设置显示外键字段

    # list_editable 设置默认可编辑字段
    # list_editable = ['title']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'userName')

    list_filter = ('userName', 'Account')  # 过滤器
    search_fields = ('userName', 'userEmail', 'create_date')  # 搜索字段
    # date_hierarchy = 'create_date'  # 详细时间分层筛选　


class RemakeAdmin(admin.ModelAdmin):
    list_display = ('id', 'speaker', 'article', 'message', 'create_date')

admin.site.register(SmallText),
admin.site.register(Blog, BlogAdmin),
admin.site.register(UserInfo, UserAdmin),
admin.site.register(Remark, RemakeAdmin)
admin.site.site_header = '机器学习后台数据管理系统'
admin.site.site_title = '后台管理'