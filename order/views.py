#! /usr/bin/env python
#coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from order.models import Order, OrderDetail
from address.models import Address
from django.template import RequestContext
from cart.views import getCart, cleanCart
import zipfile
import  sys
import os
import datetime
from datetime import *


reload(sys)
sys.setdefaultencoding("utf-8")


@login_required
def order(request):
    cart=getCart(request)
    user=request.user
    item_set=cart.cartitem_set.all()
#检查contains_digital
    is_only_digital=only_digital(item_set)
    if item_set.count()>0:
        price=0
        if is_only_digital:
            order=Order.objects.create(user=user,
                 is_only_digital=is_only_digital, address_id=0,
                 price=price, finished=True, finished_date=datetime.now())
        else:
            try:
                address=Address.objects.filter(user=user,
                    pk=request.GET['address_id'])[0]
            except:
                address=Address.objects.filter(user=user)[0]
            order=Order.objects.create(user=user, address=address,
            is_only_digital=is_only_digital, price=price)
# 对接购物车和订单
# 检查数量
        for item in item_set:
            amount=item.amount
            if amount<item.album.amount:
                detail=OrderDetail.objects.create(order=order,
                album=item.album,
                amount=amount,
                per_price=item.album.price)
                price+=detail.get_total_price()
            else:
                pass
        order.price=price
        order.save()
        cleanCart(request)
        return HttpResponseRedirect('/order/my_order/')
    else:
        raise Http404


@login_required
def my_order(request):
    order_set=Order.objects.all().filter(user=request.user).order_by('-create_date')
    return render_to_response('my_order.html',
        {'order_set': order_set},
        context_instance=RequestContext(request))


@login_required
def myorderdetail(request, my_order_id):
    order = Order.objects.get(pk=my_order_id)
    return render_to_response('order_detail.html',
        {'order': order},
        context_instance=RequestContext(request))


def finished(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.finished_date=datetime.datetime.now()
    order.finished=True
    order.save()
    print order.finished_date
    return HttpResponse('Finished Success')


file_dir=os.path.dirname(os.path.dirname(__file__))
download_dir=os.path.join(file_dir, 'music', 'media', 'download').replace('\\', '/')


def download(request, order_id):
    order = Order.objects.get(pk=order_id)
    if request.user==order.user:
        file_name=unicode(order.id)+'.rar'
        f_zip = zipfile.ZipFile(os.path.join(download_dir, file_name).replace('\\', '/'), 'w', zipfile.ZIP_STORED)
        for orderdetail in order.orderdetail_set.all():
            album_title=unicode(orderdetail.album.title)
            album=os.path.join(download_dir, album_title+'.mp3').replace('\\', '/')
            f=open(album, 'w')
            f.close()
            f_zip.write(album, album_title+'/'+album_title+'.mp3')
            os.remove(album)
        f_zip.close()
        #return HttpResponse()
        return HttpResponseRedirect('/media/download/'+file_name)
    else:
        Http404()


def only_digital(item_set):
    for item in item_set:
        if not item.album.is_digital:
            return False
    else:
        return True
