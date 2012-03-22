#! /usr/bin/env python
#coding=utf-8
from django.contrib import admin
from music.album.models import Album

class AlbumAdmin(admin.ModelAdmin):
    pass
admin.site.register(Album, AlbumAdmin)
