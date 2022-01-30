"""work2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from .views import logins, doregisters, registers, error1s, pleases, logouts, homepages, losts, losts2, losts3, create, \
    manage, wds, photo, nicknames, dell, edit, add, doadd, doedit, sells, send, reply, doreply, back, changes, \
    dochanges, ground, down

urlpatterns = [
    path('seller/please/', pleases, name='pleases'),
    path('seller/error1/', error1s, name='error1s'),
    path('seller/login/', logins, name='logins'),
    path('seller/register/', registers, name='registers'),
    path('seller/doregister/', doregisters, name='doregisters'),
    path('sellers/logout/', logouts, name='logouts'),
    path('sellers/homepage/', homepages, name='homepages'),
    path('seller/losts', losts, name='losts'),
    path('seller/losts2', losts2, name='losts2'),
    path('seller/losts3', losts3, name='losts3'),
    path('sellers/create/', create, name='create'),
    path("sellers/manage/<int:storeid>", manage, name='manage'),
    path('sellers/wd', wds, name='wds'),
    path('sellers/photo', photo, name='photos'),
    path('sellers/nickname', nicknames, name='nicknames'),
    path('sellers/dell/<int:staffid>', dell, name='dell'),
    path('sellers/edit', edit, name='edit'),
    path('sellers/add', add, name='add'),
    path('sellers/doadd', doadd, name='doadd'),
    path('sellers/doedit', doedit, name='doedit'),
    path('ueditor/', include('ueditor.urls')),
    path('sellers/sells', sells, name='sells'),
    path('sellers/send/<int:oid>', send, name='send'),
    path('sellers/reply', reply, name='reply'),
    path('sellers/doreply', doreply, name='doreply'),
    path('home/back/<int:oid>', back, name='back'),
    path('sellers/change/', changes, name='changes'),
    path('sellers/dochange/', dochanges, name='dochanges'),
    path('sellers/ground/<int:sid>', ground, name='ground'),
    path('sellers/down/<int:sid>', down, name='down'),
]
