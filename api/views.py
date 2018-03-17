from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
import time
from django.http import HttpResponse
from ContentApp.models import AttentionTable
from model.user.login import UserInfo
from common.mongohelper import get_db


@csrf_exempt
def search_home(request):
    if request.method == 'POST':
        content = request.POST.get('search_content')
        print(content)
        uid = request.COOKIES.get('user_id')
        if not uid:
            return HttpResponse('no user')
        if content:
            db = get_db()
            db.gg_search.insert({'user': uid, 'content': content,  'create_time': int(time.time())})
            return HttpResponse('ok')
        else:
            return HttpResponse('ok')


@csrf_exempt
def focus_people(request):
    if request.method == 'POST':
        uid = request.COOKIES.get('user_id')
        cencerned = request.POST.get('Concerned')
        action = request.POST.get('action')
        if uid and cencerned:
            if action == 'cencern':
                obj1 = UserInfo.objects.filter(Account=cencerned)
                for j in obj1:
                    try:
                        cer = AttentionTable()
                        cer.Concern = uid
                        cer.Concerned = j
                        cer.save()
                        return HttpResponse('ok')
                    except Exception as e:
                        print(e)
            if action == 'cancel':
                try:
                    cer = AttentionTable.objects.filter(Concern=uid, Concerned=cencerned)
                    if cer:
                        cer.delete()
                        return HttpResponse('ok')
                except Exception as e:
                    print(e)
        else:
            HttpResponse('no')
