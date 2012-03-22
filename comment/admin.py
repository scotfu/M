#! /usr/bin/env python
#coding=utf-8
from django.contrib import admin
from music.comment.models import Comment

class CommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comment, CommentAdmin)
