#! /usr/bin/env python
#coding=utf-8
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from .models import Album, Genre
from accounts.forms import AlbumForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@csrf_protect
@login_required
def add(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            Album.objects.create(
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                pic = form.pic,
                for_sale = True,
                price = form.cleaned_data['price'],
                active = True,
                amount = form.cleaned_data['amount'],
                singer = form.cleaned_data['singer'],
                year = form.cleaned_data['year'],
                genre = form.cleaned_data['genre'],
                isbn = form.cleaned_data['isbn'],
                company = form.cleaned_data['company'],
                store = form.cleaned_data['store'])
            return HttpResponse('success')
    else:
        form = AlbumForm()
    return render_to_response('album_form.html', {
        'form': form,
        }, context_instance=RequestContext(request))


def genre(request, genre_name):
    try:
        genre = Genre.objects.get(name=genre_name)
        album_list = Album.objects.all().filter(genre=genre)
    except:
        album_list = None
    if  album_list:
        return render_to_response(
            'album_list.html', 
            {
             'object_list': my_pageination(request, album_list),
             'genre': genre_name
             },
            context_instance=RequestContext(request))
    else:
        return render_to_response(
            'album_list.html', 
            {
            'object_list': album_list,
            'genre': genre_name
            },
            context_instance=RequestContext(request))


def search(request, key_word=''):
    try:
        album_list = Album.objects.all().filter(Q(title__icontains=key_word)|
                                                Q(singer__icontains=key_word)|
                                                Q(description__icontains=key_word))
    except:
        album_list = None
    if album_list:
        return render_to_response('search_result.html', {
            'object_list': my_pageination(request, album_list),
            'key_word': key_word},
            context_instance=RequestContext(request))
    else:
        return render_to_response('search_result.html', {
            'object_list': album_list,
            'key_word': key_word},
            context_instance=RequestContext(request))


def indexview(request):
    album_list = Album.objects.all()
    return render_to_response(
        'album_list.html',
        {'object_list': my_pageination(request, album_list)},
        context_instance=RequestContext(request))


def albumdetailview(request, album_id):
    try:
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist:
        raise Http404
    buy = False # Flag determines that if a cusomer has bought this album before
    if '_auth_user_id' in request.session:
        user = request.user
        for order in user.order_set.all():
            try:
                order.orderdetail_set.get(album=album)
                buy = True
            except:
                pass
    return render_to_response('album_detail.html', {
        'album': album,
        'buy': buy,
        }, context_instance=RequestContext(request))


def my_pageination(request, object_list):
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects = paginator.page(paginator.num_pages)
    return objects
