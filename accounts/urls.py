#! /usr/bin/env python
#coding=utf-8
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('accounts.views',
    url(r'^$', 'modifyview'),
    url(r'^quicklogin/$', 'quickloginview'),
    url(r'^login/$', 'loginview'),
    url(r'^register/$', 'register'),
    url(r'^logout/$', 'logoutview'),
    )

urlpatterns += patterns('',
    url(r'^register/success/$',\
        TemplateView.as_view(template_name='register_success.html')),
    )
