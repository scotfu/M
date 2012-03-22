#! /usr/bin/env python
#coding=utf-8
from django.contrib import admin
from music.address.models import Address

class AddressAdmin(admin.ModelAdmin):
    pass
admin.site.register(Address, AddressAdmin)
