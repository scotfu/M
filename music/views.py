#! /usr/bin/env python
#coding=utf-8
from django.http import HttpResponseRedirect


def download(request):
    
    return HttpResponseRedirect('/media/download/1.zip')
