"""
@author: laurel
@file: admin.py.py
@time: 2019/05/15
@description: tools
"""

from django.shortcuts import render, render_to_response
from django.http import JsonResponse,HttpResponse, HttpResponseRedirect
from syapp.models import YsArticle, Ips, Logs
from django import forms
from syapp.models import UserMain
from django.db.models import Sum
import time,hashlib,os,datetime
import json,math

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def geoDistanceLayout(request):
    return render(request, 'tools.html', {})

def geoDistance(request):
    geohash1 = request.GET.get('geohash1')
    geohash2 = request.GET.get('geohash2')
    hashlist1 = geohash1.split(',')
    hashlist2 = geohash2.split(',')
    if len(hashlist1) != 2 or len(hashlist2) != 2:
        return HttpResponse(-1)
    return HttpResponse(EarthDistance(float(hashlist1[1]), float(hashlist1[0]), float(hashlist2[1]), float(hashlist2[0])))

def EarthDistance(lat1,lng1,lat2,lng2):
    radius = float(6371000)
    rad = math.pi/180.0
    lat1 = lat1*rad
    lng1 = lng1*rad 
    lat2 = lat2*rad 
    lng2 = lng2*rad 
    theta = lng2-lng1
    dist = math.acos(math.sin(lat1)*math.sin(lat2)+math.cos(lat1)*math.cos(lat2)*math.cos(theta))
    return dist*radius


