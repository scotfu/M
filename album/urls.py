#! /usr/bin/env python
#coding=utf-8
from django.conf.urls import patterns, url
from album.models import Album
from django.views.generic import ListView
from album.views import albumdetailview
urlpatterns = patterns('album.views',
    url(r'^add/$', 'add'),
    url(r'^$', 'indexview'),
    url(r'^(?P<album_id>\d+)/$', albumdetailview),
    url(r'^genre/(?P<genre>\w+)/$', 'genre'),
    url(r'^search/(?P<key_word>\w+)/$', 'search'),
    url(r'^search/$', 'search'),
    )
