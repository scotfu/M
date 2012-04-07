#! /usr/bin/env python
#coding=utf-8
from django.contrib import admin
from album.models import Album, Genre


class AlbumAdmin(admin.ModelAdmin):
    list_filter = ('price', 'singer','amount')
    list_display = ('id','title','singer','price','amount','active')
    search_fields = ['singer','title']
    list_editable=('price','amount')
    fieldsets=(
        (None,{
            'fields':('title','price','amount','for_sale','active')
            }),
        ('More options',{
            'classes':('collapse',),
            'fields':('description','pic','year','singer',
                      'genre','company','isbn','store')
            }),

        )

class GenreAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_editable=('name',)


admin.site.register(Album, AlbumAdmin)
admin.site.register(Genre,GenreAdmin)
