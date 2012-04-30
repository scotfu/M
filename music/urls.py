#! /usr/bin/env python
#coding=utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template', {
        'template': 'index.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^album/', include('album.urls')),
    url(r'^comment/', include('comment.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^address/', include('address.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^order/', include('order.urls')),
    )
if settings.DEBUG:
    urlpatterns += patterns('',
                url(r"^media/(?P<path>.*)$", \
                    "django.views.static.serve", \
                    {"document_root": settings.MEDIA_ROOT,}),
    )
    
