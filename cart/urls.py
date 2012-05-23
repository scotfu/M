#! /usr/bin/env python
#coding=utf-8
from django.conf.urls import url, patterns

urlpatterns = patterns('cart.views',
    url('^$', 'show'),
    url('^add/(?P<album_id>\d+)/$', 'add_to_cart'),
    url('^delete/(?P<album_id>\d+)/$', 'delete_one_by_id'),
    url('^cart_add/(?P<album_id>\d+)/$', 'add_one_by_id'),
    url('^delete_album/(?P<album_id>\d+)/$', 'delete_by_id'),
    url('^pre_order/$', 'pre_order'),
    url('^clean/$', 'clean'),
    )
