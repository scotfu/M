#! /usr/bin/env python
#coding=utf-8
from django.conf.urls import patterns, url
from .views import RegisterSuccessView

urlpatterns = patterns('accounts.views',
    url(r'^$', 'modifyview'),
    url(r'^quicklogin/$', 'quickloginview'),
    url(r'^login/$', 'loginview'),
    url(r'^register/$', 'register'),
    url(r'^logout/$', 'logoutview'),
    )

urlpatterns += patterns('',
    url(r'^register/success/$',RegisterSuccessView.as_view()),
    )
