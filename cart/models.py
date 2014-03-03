#! usr/bin/env python
#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from albums.models import Album


class Cart(models.Model):
    user=models.ForeignKey(User)

    class Meta:
        verbose_name_plural = "购物车"

    def __unicode__(self):
        return self.user.username

    def total_item(self):
        return self.cartitem_set.count()


class CartItem(models.Model):
    cart=models.ForeignKey(Cart)
    album=models.ForeignKey(Album)
    amount=models.IntegerField(max_length=10)

    class Meta:
        verbose_name_plural = "购物车明细"

    def __unicode__(self):
        return self.album.title

    def get_items_price(self):
        return self.album.price*self.amount


class Item(object):

    def setAlbum(self, album):
        self.album=album

    def getAlbum(self):
        return self.album

    def setAmount(self, amount):
        self.amount = amount

    def getAmount(self):
        return  self.amount

    def __unicode__(self):
        return '%s:%s' %(self.album, self.amount)
