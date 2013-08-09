#! /usr/bin/env python
#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from entry.models import Entry

class Store(models.Model):
    name=models.CharField(max_length=100)
    owner=models.ForeignKey(User)
    create_date=models.DateField(auto_now_add=True)
    entry=models.ForeignKey(Entry)
    def __unicode__(self):
        return self.name
