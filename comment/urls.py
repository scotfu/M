#! /usr/bin/env python
#coding=utf-8
from django.conf.urls import patterns, url


urlpatterns = patterns('comment.views',
    url(r'^add/$', 'add'),
    )
