from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from syapp.models import UserMain, YsArticle
import time,hashlib
import json
# jujiaodata.com.
# 生成列表页


class UserForm(forms.Form):
    username = forms.CharField(label='username',max_length=50)
    password = forms.CharField(label='password',widget=forms.PasswordInput())
    
def index(request):
    diariesList = []
    lastId=request.GET.get('lastid',default='0')
    once=request.GET.get('once',default='10')
    try:
        last = int(lastId)
        one = int(once)
        articles = YsArticle.objects.filter(reserve = '1').order_by('-id')[last-one:last]
        for article in articles:
            dic = {}
            dic['content_id'] = str(article.id)
            dic['cover'] = article.cover
            dic['title'] = article.title
            dic['meta'] = article.createtime.strftime("%Y-%m-%d %H:%M:%S")
            diariesList.append(dic)
    except Exception as e:
        HttpResponse(e)
    return HttpResponse(json.dumps(diariesList))

def detail(request):
    context = {}
    contentid=request.GET.get('contentid',default='0')
    try:
        contentid = int(contentid)
        orm_obj = YsArticle.objects.get(id=contentid)
        if orm_obj is None:
            return render(request, 'detail.html', context) 
        context['htmlBody'] = orm_obj.article
        context['time'] = orm_obj.articletime
        context['category'] = orm_obj.category
        context['title'] = orm_obj.title
        context['source'] = fetchSource(orm_obj.source)
        updateReadTime(contentid, orm_obj)
    except Exception as e:
        HttpResponse(e)
    return render(request, 'detail.html', context)

def login(request):
    if checkLoginStatus(request):
        response = HttpResponseRedirect('/')
        return response
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            hash_obj = hashlib.md5()
            hash_obj.update(password.encode('utf-8'))
            md5_pwd = hash_obj.hexdigest()

            user = UserMain.objects.filter(username__exact=username,password__exact=md5_pwd)

            if user:
                response = HttpResponseRedirect('/')
                response.set_cookie('username',username,3600)
                response.set_cookie('pwd',md5_pwd,3600)
                return response
            else:
                return HttpResponse('username/password error! please retry!')
    else:
        userform = UserForm()
    return render(request, 'login.html',{'userform':userform})

def regist(request):
    if not checkLoginStatus(request):
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']

            check = UserMain.objects.filter(username__exact=username)
            if check:
                return HttpResponse('该用户名已存在,请更换用户名重试！')

            hash_obj = hashlib.md5()
            hash_obj.update(password.encode('utf-8'))
            md5_pwd = hash_obj.hexdigest()
            dateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            UserMain.objects.create(username=username,password=md5_pwd,date = dateTime)
            return HttpResponseRedirect('/login/')
    else:
        userform = UserForm()
    return render(request,'regist.html',{'userform':userform})

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

def logout(request):
    response = HttpResponseRedirect('/login/')
    response.delete_cookie('username')
    response.delete_cookie('pwd')
    return response

def fetchSource(source):
    source = int(source)
    comeFrom = '养生健康网' #gjk88
    if source==2:
        comeFrom = '中华养生网' #cnys
    if source==3:
        comeFrom = '大众养生网' #cndzys
    return comeFrom

def updateReadTime(contentid, orm_obj):
    oldReadTimes = int(orm_obj.readtimes)
    newReadTimes = oldReadTimes+1
    orm_obj.readtimes = newReadTimes
    orm_obj.save()

def fuzzySearch(request):
    diariesList = []
    keyword=request.GET.get('keyword')
    try:
        articles = YsArticle.objects.filter(title__contains=keyword.strip())
        for article in articles:
            dic = {}
            dic['content_id'] = str(article.id)
            dic['cover'] = article.cover
            dic['title'] = article.title
            dic['meta'] = article.createtime.strftime("%Y-%m-%d %H:%M:%S")
            diariesList.append(dic)
    except Exception as e:
        HttpResponse(e)
    return HttpResponse(json.dumps(diariesList))
