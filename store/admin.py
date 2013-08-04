#! /usr/bin/env python
#coding=utf-8
from django.contrib import admin
from store.models import Store


class StoreAdmin(admin.ModelAdmin):
    pass
admin.site.register(Store, StoreAdmin)
