"""miniP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import syapp.views as sy
import V.backend as bk
import V.admin as ad
import V.tool as tl

urlpatterns = [
    url(r'^$', ad.admin),
    url(r'^login/', bk.login),
    url(r'^account/', bk.regist),
    url(r'^admin/', admin.site.urls),
    url(r'^getlist/', bk.index),
    url(r'^getdetail/', bk.detail),
    url(r'^logout/', bk.logout),
    url(r'^model/', ad.showModel),
    url(r'^query/', ad.queryDb),
    url(r'^putty/', ad.putty),
    url(r'^handle/', ad.handleShell),
    url(r'^search/', bk.fuzzySearch),
    url(r'^showchart/', ad.showChart),
    url(r'^tools/', tl.geoDistanceLayout),
    url(r'^caldistance/', tl.geoDistance)
]
