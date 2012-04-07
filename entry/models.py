#! /usr/bin/env python
#coding=utf-8
from django.db import models


class Entry(models.Model):
    name=models.CharField(max_length=100)
    def __unicode__(self):
        return self.name
