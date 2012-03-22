#! /usr/bin/env python
#coding=utf-8
from django.http import HttpResponse
from album.models import Album
def index(request):
    albums=Album.objects.all()
    return HttpResponse(albums)