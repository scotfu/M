#! /usr/bin/env python
#coding=utf-8
from django.db import models
from store.models import Store


class Album(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    description = models.TextField(max_length=512, verbose_name='简介')
    pic=models.FileField(upload_to='upload', verbose_name='封面')
    for_sale=models.BooleanField(default=True, verbose_name='是否销售')
    price=models.DecimalField(max_digits=5, decimal_places=2,
                                        verbose_name='价格')
    active=models.BooleanField(default=True)
    amount=models.IntegerField(verbose_name='数量')
    singer=models.CharField(max_length=50, verbose_name='歌手')
    year=models.IntegerField(max_length=4, verbose_name='年')
    genre=models.ForeignKey('Genre', verbose_name='风格')
    isbn=models.CharField(max_length=30)
    company=models.CharField(max_length=30, verbose_name='发行方')
    create_date=models.DateField(auto_now_add=True)
    modify_date=models.DateField(auto_now=True)
    store=models.ForeignKey(Store, blank=True)
    is_digital=models.BooleanField(default=True,verbose_name='数字版')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "专辑"


class Genre(models.Model):
    name=models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "风格"

    def __unicode__(self):
        return self.name
