# /usr/bin/dev python
#coding=utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from album.models import Album
from cart.models import CartItem, Cart, Item
import re


def getCart(request):
    if  '_auth_user_id' in request.session:
        try:
            cart=Cart.objects.get(user=request.user)
        except ObjectDoesNotExist:
            cart=Cart.objects.create(user=request.user)
    else:
        if 'cart' not in request.session:
            request.session['cart']={}
        cart=request.session['cart']
    return cart


def cleanCart(request):
    if '_auth_user_id' in request.session:
        cart=Cart.objects.get(user=request.user)
        for item in cart.cartitem_set.all():
            item.delete()
    else:
        request.session['cart']={}


def cartMerge(user_cart, session_cart):
    if  session_cart:
        for album_key in session_cart:
            amount=session_cart[album_key]
            try:
                f_item = user_cart.cartitem_set.get(album=album_key)
                f_item.amount+=amount
                f_item.save()
            except ObjectDoesNotExist:
                CartItem.objects.create(cart=user_cart,
                    album=album_key, amount=amount)
        session_cart={}
    return user_cart


def show(request):
    cart = getCart(request)
    item_set=[]
    if '_auth_user_id' in request.session:
        item_set=cart.cartitem_set.all()
    else:
        if  cart:
            for album_key in cart:
                item=Item()
                item.album=album_key
                item.amount=cart[album_key]
                item_set.append(item)
            for item in item_set:
                print item.album
    return render_to_response('my_cart.html', {
        'item_set': item_set},
        context_instance=RequestContext(request))


def add_to_cart(request, album_id):
    cart=getCart(request)
#专辑是否存在
    try:
        album=Album.objects.get(pk=album_id)
    except:
        raise Http404
#数量是否选择
    if 'amount' in request.GET:
        if not re.search(r'\d+$', request.GET['amount']):
            raise Http404
        else:
            amount=int(request.GET['amount'])
    else:
        amount=1
#是否已有该专辑
    if '_auth_user_id' in request.session:
        try:
            item = cart.cartitem_set.get(album=album)
            item.amount+=amount
            item.save()
        except ObjectDoesNotExist:
            item=CartItem.objects.create(cart=cart, album=album, amount=amount)
#匿名用户购物车
    else:
        if album in cart:
            cart[album]+= amount
        else:
            cart[album]=amount
        item=Item()
        item.album=album
        item.amount=cart[album]
        request.session['cart']=cart
    return render_to_response('new_item.html',
        {'item': item,
        'amount': amount},
        context_instance=RequestContext(request))


def delete_one_by_id(request, album_id):
    delete_album=Album.objects.get(pk=album_id)
    cart=getCart(request)
    if '_auth_user_id' in request.session:
        try:
            item=cart.cartitem_set.get(album=delete_album)
            item.amount-=1
            item.save()
        except:
            raise Http404
        if item.amount==0:
            item.delete()
    else:
        if cart[delete_album]>0:
            cart[delete_album]-=1
            if cart[delete_album]==0:
                del cart[delete_album]
            request.session['cart']=cart
        else:
            return HttpResponse('Error')
    return HttpResponseRedirect('/cart/')


def add_one_by_id(request, album_id):
    add_album=Album.objects.get(pk=album_id)
    cart=getCart(request)
    if '_auth_user_id' in request.session:
        try:
            item=cart.cartitem_set.get(album=add_album)
            item.amount+=1
            item.save()
        except:
            raise Http404
    else:
        if cart[add_album]>0:
            cart[add_album]+=1
            request.session['cart']=cart
        else:
            return HttpResponse('Error')
    return HttpResponseRedirect('/cart/')


def delete_by_id(request, album_id):
    delete_album=Album.objects.get(pk=album_id)
    cart=getCart(request)
    if '_auth_user_id' in request.session:
        try:
            item=cart.cartitem_set.get(album=delete_album)
            item.delete()
        except:
            raise Http404
    else:
        try:
            del cart[delete_album]
            request.session['cart']=cart
        except:
            return HttpResponse('Error')
    return HttpResponseRedirect('/cart/')


def clean(request):
    cleanCart(request)
    return HttpResponseRedirect('/cart/')


@login_required
def pre_order(request):
    cart=getCart(request)
    item_set=cart.cartitem_set.all()
    price=0
    is_only_digital=only_digital(item_set)
    print is_only_digital
    for item in item_set:
        items_price=item.get_items_price()
        price+=items_price
    address_set=request.user.address_set.all()
    return render_to_response('pre_order.html',
        {'item_set': item_set,
        'price': price,
        'address_set': address_set,
        'is_only_digital': is_only_digital},
        context_instance=RequestContext(request))


def only_digital(item_set):
    for item in item_set:
        if not item.album.is_digital:
            return False
    else:
        return True
