#! /usr/bin/env python
#coding=utf-8
from django.contrib import admin
from order.models import Order, OrderDetail


class OrderDetailInline(admin.TabularInline):
    model=OrderDetail
    extra=0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'price', 'create_date', 'finished')
    list_filter = ('user', 'create_date')
    inlines = [OrderDetailInline]
    search_fields = ['user']


class OrderDetailAdmin(admin.ModelAdmin):
    list_filter = ('album', )
    list_display = ('id', 'album', 'amount', 'get_total_price', 'order')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
