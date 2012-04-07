#! /usr/bin/env python
#coding=utf-8
from django.contrib import admin
from cart.models  import Cart, CartItem


class CartInline(admin.TabularInline):
    model=CartItem
 #   filter_horizontal = ('albums')
    extra=3


class CartAdmin(admin.ModelAdmin):
    inlines = [CartInline]
    list_display=('id', 'user', 'total_item')
    search_fields = ['user']
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
