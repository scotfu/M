#! /usr/bin/env python
#coding=utf-8
from django.db import models

class Album(models.Model):
    short_description = models.CharField(max_length=50)
    description = models.CharField(max_length=512)
    for_sale=models.BooleanField()
    for_sale_price=models.DecimalField(max_digits=5, decimal_places=2)
    active=models.BooleanField()
    amount=models.IntegerField()
    singer=models.CharField(max_length=50)
    year=models.DateField()
    genre=models.CharField(max_length=20)
    isbn=models.CharField(max_length=30)
    company=models.CharField(max_length=30)
    create_date=models.DateField(auto_now_add=True)
    modify_date=models.DateField(auto_now=True)
    def __unicode__(self):
        return self.short_description