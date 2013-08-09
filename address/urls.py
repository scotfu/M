#! /usr/bin/env python
#coding=utf-8
from django.conf.urls import patterns, url
from address.views import AddressListView

urlpatterns = patterns('address.views',
    url(r'^add/', 'save'),
    url(r'^save/', 'save'),
    url(r'^modify/(?P<address_id>\d+)/$', 'save'),
    url(r'^$', AddressListView.as_view()),
    )
