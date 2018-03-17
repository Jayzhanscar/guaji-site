from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from model.user.login import UserInfo
from common.mongohelper import get_db
from ContentApp.models import Blog
from django.core import serializers
# Create your views here.


# 导航中短词的搜索 // 根据key去搜索

@csrf_exempt
def index_1(request):
    userid = request.COOKIES.get('user_id')
    p = UserInfo.objects.filter(Account=userid)
    return render(request, 'show/show_1.html', locals())


@csrf_exempt
def index_2(request):
    userid = request.COOKIES.get('user_id')
    p = UserInfo.objects.filter(Account=userid)
    return render(request, 'show/show_2.html', locals())


@csrf_exempt
def index_3(request):
    userid = request.COOKIES.get('user_id')
    p = UserInfo.objects.filter(Account=userid)
    return render(request, 'show/show_3.html', locals())


@csrf_exempt
def process(request):
    userid = request.COOKIES.get('user_id')
    p = UserInfo.objects.filter(Account=userid)
    return render(request, 'show/jinzhan.html', locals())


@csrf_exempt
def transform(request):
    userid = request.COOKIES.get('user_id')
    p = UserInfo.objects.filter(Account=userid)
    return render(request, 'show/jiaoliu.html', locals())


@csrf_exempt
def chat(request):
    """
    :param request: 
    :param search: 
    :return: 
    """
    user_id = request.COOKIES.get('user_id')
    max = 0
    search_content = ''
    now_search = []
    p = UserInfo.objects.filter(Account=user_id)
    try:
        db = get_db()
        b = db.gg_search.find({'user': user_id})
        for j in b:
            if max < j['create_time']:
                max = j['create_time']
                search_content = j['content']
                now_search.append(search_content)
                user_obj = UserInfo.objects.filter(userName__contains=search_content)[0:3]
                if not user_obj:
                    user_obj = UserInfo.objects.all()[0:3]
                wz = Blog.objects.filter(title__contains=search_content)
                count = wz.count()
    except Exception as e:
        print(e)
    for i in p:
        img_name = i.img.url
    if request.method == 'POST':
        action = request.POST.get('action', None)
        if action == 'yh':
            users = UserInfo.objects.filter(userName__contains=search_content)
            data = serializers.serialize('json', users)
            print(data)
            return HttpResponse(data)

    return render(request, 'show/luntan.html', locals())