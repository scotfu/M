#! /usr/bin/env python
#coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    postal_code=models.CharField(max_length=10)
    address=models.CharField(max_length=126)
    name=models.CharField(max_length=30)
    user=models.ForeignKey(User)

    def __unicode__(self):
        return self.address

    class Meta:
        verbose_name_plural = "地址"
