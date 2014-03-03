#! /usr/bin/env python
#coding=utf-8
from django.conf.urls import patterns, url
from albums.views import albumdetailview
urlpatterns = patterns('albums.views',
    url(r'^add/$', 'add'),
    url(r'^$', 'indexview'),
    url(r'^(?P<album_id>\d+)/$', albumdetailview),
    url(r'^genre/(?P<genre_name>.+)/$', 'genre'),
    url(r'^search/(?P<key_word>.+)/$', 'search'),
    url(r'^search/$', 'search'),
    )
