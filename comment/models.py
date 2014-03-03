#! /usr/bin/env python
#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from albums.models import Album


class Comment(models.Model):

    title=models.CharField(max_length=30)
    content=models.TextField(max_length=512)
    create_time=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User)
    album=models.ForeignKey(Album)

    class Meta:
        verbose_name_plural = "专辑评论"

    def __unicode__(self):
        return self.title
