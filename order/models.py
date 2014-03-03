#! /usr/bin/env python
#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from address.models import Address
from albums.models import Album


class Order(models.Model):
    user=models.ForeignKey(User, verbose_name='用户')
    address=models.ForeignKey(Address, verbose_name='收货地址')
    create_date=models.DateTimeField(auto_now_add=True, verbose_name='时间')
    finished=models.BooleanField('完成', False)
    finished_date=models.DateTimeField('完成日期', null=True)
    price=models.DecimalField('总价', max_digits=5, decimal_places=2)
    is_only_digital=models.BooleanField(default=True,verbose_name='仅数字版')

    class Meta:
        verbose_name_plural = "订单"

    def __unicode__(self):
        return self.user.username


class OrderDetail(models.Model):
    order=models.ForeignKey(Order)
    album=models.ForeignKey(Album, verbose_name='专辑')
    amount=models.IntegerField(max_length=10, verbose_name='数量')
    per_price=models.DecimalField(max_digits=5, decimal_places=2,
                                  verbose_name='单价')

    class Meta:
        verbose_name_plural = "订单明细"

    def get_total_price(self):
        return self.per_price*self.amount

    def __unicode__(self):
        return self.album.title
