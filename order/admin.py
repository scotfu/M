#! /usr/bin/env python
#coding=utf-8
from django.contrib import admin
from order.models import Order, OrderDetail


class OrderDetailInline(admin.TabularInline):
    model=OrderDetail
    extra=0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderDetailInline]
    search_fields = ['user']

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail)
