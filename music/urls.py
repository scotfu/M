#! /usr/bin/env python
#coding=utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import TemplateView

admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^album/', include('albums.urls')),
    url(r'^comment/', include('comment.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^address/', include('address.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^order/', include('order.urls')),
    )
#if settings.DEBUG:
urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, },
        name='media'),
        )
urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT, },
        name='static'),
        )


        
