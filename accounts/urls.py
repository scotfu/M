#! /usr/bin/env python
#coding=utf-8
from django.conf.urls import patterns, url


urlpatterns = patterns('accounts.views',
    url(r'^$', 'modifyview'),
    url(r'^quicklogin/$', 'quickloginview'),
    url(r'^login/$', 'loginview'),
    url(r'^register/$', 'register'),
    url(r'^logout/$', 'logoutview'),
    )

urlpatterns += patterns('',
    url(r'^register/success/$',
        'django.views.generic.simple.direct_to_template', {
        'template': 'register_success.html'}),
    )
