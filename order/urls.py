#! /usr/bin/env python
#coding=utf-8
from django.conf.urls import patterns, url


urlpatterns = patterns('order.views',
    url(r'^$', 'order'),
    url(r'^my_order/$', 'my_order'),
    url(r'^my_order/(?P<my_order_id>\d+)/$', 'myorderdetail'),
    url(r'^(?P<order_id>\d+)/finished/$', 'finished'),
    url(r'^(?P<order_id>\d+)/download/$', 'download'),
    )
