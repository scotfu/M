#! /usr/bin/env python
#coding=utf-8
from django.http import HttpResponseRedirect, Http404
from accounts.forms import CommentForm
from comment.models import Comment
from album.models import Album
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

@csrf_protect
@login_required
def add(request):
    path=request.path
    if request.method=='POST':
         form=CommentForm(request.POST)
         print form
         if form.is_valid():
             Comment.objects.create(user=request.user,
                album=Album.objects.get(pk=request.POST['album']),
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
