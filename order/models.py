#! /usr/bin/env python
#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from address.models import Address
from album.models import Album


class Order(models.Model):
    user=models.ForeignKey(User)
    address=models.ForeignKey(Address)
    create_date=models.DateTimeField(auto_now_add=True)
    finished=models.BooleanField(False)
    finished_date=models.DateTimeField(null=True)
    price=models.DecimalField(max_digits=5, decimal_places=2)
            


class OrderDetail(models.Model):
    order=models.ForeignKey(Order)
    album=models.ForeignKey(Album)
    amount=models.IntegerField(max_length=10)
    per_price=models.DecimalField(max_digits=5, decimal_places=2)

    def get_total_price(self):
        return self.per_price*self.amount
