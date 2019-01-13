"""
@author: laurel
@file: admin.py.py
@time: 2018/11/2010:51 PM
@description: 
"""

from django.shortcuts import render, render_to_response
from django.http import JsonResponse,HttpResponse, HttpResponseRedirect

# jujiaodata.com.
# 后台管理
from syapp.models import YsArticle, Ips, Logs
from django import forms
from syapp.models import UserMain
from django.db.models import Sum
import time,hashlib,os,datetime
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def admin(request):
    if not checkLoginStatus(request):
        return HttpResponseRedirect('/login/')
    # log = Logs(log = "helo")
    # log.save()
    # 获取今日新增
    timestamp = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    logTday = Logs.objects.exclude(createtime__lt=timestamp).count()
    # ipTday = '-'
    ysTday = YsArticle.objects.exclude(createtime__lt=timestamp).count()

    show = {}
    ysTotal = YsArticle.objects.count()
    ipTotal = Ips.objects.count()
    logTotal = Logs.objects.count()
    show['ystotal'] = ysTotal
    show['iptotal'] = ipTotal
    show['logtotal'] = logTotal

    show['ystoday'] = ysTday
    show['logtoday'] = logTday
    show['totalreadtimes'] = YsArticle.objects.all().aggregate(Sum('readtimes'))['readtimes__sum']
    return render(request, 'admin.html', {'show': show})

def showChart(request):
    if not checkLoginStatus(request):
        return HttpResponseRedirect('/login/')
    dateDelta = 7
    dateOfTday = datetime.datetime.now().date()
    dateOf7DaysAgo = dateOfTday - datetime.timedelta(weeks=1)
    dataOf7Days = YsArticle.objects.filter(createtime__gte=dateOf7DaysAgo, createtime__lte=dateOfTday+datetime.timedelta(days=1))
    # dataOf7Days = YsArticle.objects.all()
    readtimelist = []
    deltalist = []
    for dta in range(dateDelta):
        #获取阅读量
        startDate = dateOfTday-datetime.timedelta(dateDelta-dta-1)
        readtimes = dataOf7Days.filter(createtime__range=(startDate, startDate + datetime.timedelta(days=1))).aggregate(Sum('readtimes'))['readtimes__sum']
        delta = dataOf7Days.filter(createtime__range=(startDate, startDate + datetime.timedelta(days=1))).count()
        readtimelist.append(readtimes if readtimes is not None else 0)
        deltalist.append(delta if delta is not None else 0)

    show = {}
    show['readtime'] = readtimelist
    show['delta'] = deltalist

    return JsonResponse(show)

def showModel(request):
    if not checkLoginStatus(request):
        return HttpResponseRedirect('/login/')
    return render(request, 'showdb.html')

def queryDb(request):
    if not checkLoginStatus(request):
        return HttpResponseRedirect('/login/')
    import json
    tablename = request.GET.get('tablename')
    offset = int(request.GET.get('offset'))
    if tablename == 'YsArticle':
        resList = YsArticle.objects.order_by('-id')
        offset = offset%len(resList)
        res = resList[offset]
        content = res.article
    else:
        resList = Logs.objects.order_by('-id')
        offset = offset%len(resList)
        res = resList[offset]
        content = res.log

    # return HttpResponse(json.dumps({'content': content}), content_type='application/json')
    # return render(request, 'showdb.html', {'content': content})
    return JsonResponse({'content': content})

#检测登陆状态#
def checkLoginStatus(request):
    if (not 'username' in request.COOKIES) or (not 'pwd' in request.COOKIES):
        return False
    username = request.COOKIES['username']
    md5_pwd = request.COOKIES['pwd']
    user = UserMain.objects.filter(username__exact=username,password__exact=md5_pwd)
    if user:
        return True 
    else:
        return False

def putty(request):
    if not checkLoginStatus(request):
        return HttpResponseRedirect('/login/')
    resp = {}
    order = 'ls '+BASE_DIR+'/extern'
    resp['filelist'] = os.popen(order).read()
    resp['filelist'] = '<br>'.join(resp['filelist'].split())
    return render(request, 'putty.html', resp)

#handle shell
def handleShell(request):
    backupDirPath = os.path.join(BASE_DIR, 'extern', 'backup')
    filename = request.GET.get('filename')
    tag = request.GET.get('function')
    if filename is None or filename=='':
        order = 'ls '+BASE_DIR+'/extern'
        res = os.popen(order).read().split()
        response = '<br>'.join(res)
        return HttpResponse(response)
    if tag=='0':
        order = 'python '+ os.path.join(BASE_DIR, 'extern', filename)
        res = os.popen(order).read()
        return HttpResponse(res.replace('\n', '<br>'))
    elif tag=='1':
        order = 'cat '+ os.path.join(BASE_DIR, 'extern', filename)
        res = os.popen(order).read()
        return HttpResponse(res)
    elif tag=='2':
        content = request.GET.get('filecontent')
        if content is not None:
            content = processContent(content)
        if not os.path.exists(backupDirPath):
            os.mkdir(backupDirPath)
        oldFilePath = os.path.join(BASE_DIR, 'extern', filename)
        newFilePath = os.path.join(backupDirPath, filename+str(time.time())+'.bak')
        order = 'mv %s %s'%(oldFilePath, newFilePath)
        # order = 'touch a.py'
        result = os.system(order)
        saveFileOrder = r'echo "%s">%s'%(content, oldFilePath)
        res = os.popen(saveFileOrder)
        return HttpResponse(res)

#处理文件格式
def processContent(cont):
    return cont.replace('"', "'").replace('\t', '    ')

