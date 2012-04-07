#! /usr/bin/env python
#coding=utf-8
from django.db import models
from store.models import Store


class Album(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=512)
    pic=models.FileField(upload_to='upload')
    for_sale=models.BooleanField(default=True)
    price=models.DecimalField(max_digits=5, decimal_places=2)
    active=models.BooleanField(default=True)
    amount=models.IntegerField()
    singer=models.CharField(max_length=50)
    year=models.IntegerField(max_length=4)
    genre=models.ForeignKey('Genre')
    isbn=models.CharField(max_length=30)
    company=models.CharField(max_length=30)
    create_date=models.DateField(auto_now_add=True)
    modify_date=models.DateField(auto_now=True)
    store=models.ForeignKey(Store)

    def __unicode__(self):
        return self.title


class Genre(models.Model):
    name=models.CharField(max_length=20)

    def __unicode__(self):
        return self.name
