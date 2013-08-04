#! /usr/bin/env python
#coding=utf-8
from django.contrib import admin
from address.models import Address

class AddressAdmin(admin.ModelAdmin):
    list_display=('id','user','postal_code','address')
admin.site.register(Address, AddressAdmin)
