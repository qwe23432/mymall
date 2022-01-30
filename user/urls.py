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
from django.contrib import admin
from django.urls import path

from .views import login, doregister, register, error1, please, logout, homepage, lost, lost3, lost2, guide, staff_, wd, \
    nickname, photo, buy, incart, address_, address__, myorder, uback, receive, mycart, homepage__, expression, store_, \
    search, change, dochange, dell_, recommend, past, rmb, order

urlpatterns = [
    path('please/', please, name='please'),
    path('error1/', error1, name='error1'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('doregister/', doregister, name='doregister'),
    path('home/logout/', logout, name='logout'),
    path('homepage/<int:home>', homepage, name='homepage'),
    path('lost/', lost, name='lost'),
    path('lost2/', lost2, name='lost2'),
    path('lost3/', lost3, name='lost3'),
    path('', guide, name='guide'),
    path('home/staff/<int:sid>', staff_, name='staff'),
    path('home/wd/', wd, name='wd'),
    path('home/nickname/', nickname, name='nickname'),
    path('home/photo/', photo, name='photo'),
    path('home/buy/<int:sid>', buy, name='buy'),
    path('home/incart/<int:sid>', incart, name='incart'),
    path('home/address/<int:sid>', address_, name='address'),
    path('home/address_/', address__, name='address_'),
    path('home/myorder/', myorder, name='myorder'),
    path('home/mycart/', mycart, name='mycart'),
    path('home/uback/<int:oid>', uback, name='uback'),
    path('home/receive/<int:oid>', receive, name='receive'),
    path('homepage/', homepage__, name='homepage__'),
    path('home/expression/<int:sid>', expression, name='expression'),
    path('home/store/<int:storeid>', store_, name='store_'),
    path('home/search/', search, name='search'),
    path('home/change/', change, name='change'),
    path('home/dochange/', dochange, name='dochange'),
    path('home/dell/<int:eid>',dell_,name='dell_'),
    path('home/recommend/',recommend,name='recommend'),
    path('home/past/',past,name='past'),
    path('home/rmb/', rmb, name='rmb'),
    path('home/order/',order,name="order"),
]
