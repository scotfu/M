#! /usr/bin/env python
#coding=utf-8
from django.contrib import admin
from comment.models import Comment


class CommentAdmin(admin.ModelAdmin):
     list_display = ('id', 'album', 'user','create_time')
     list_filter = ('album', 'user')
admin.site.register(Comment,CommentAdmin)
