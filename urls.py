#! /usr/bin/env python
#coding=utf-8
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'album.views.index'),
    #(r'^album/', include('album.urls')),
    )