#! /usr/bin/env python
#coding=utf-8
#url(r'^$', 'order'),
#url(r'^my_order/$', 'my_order'),
#url(r'^my_order/(?P<my_order_id>\d+)/$', 'myorderdetail'),
#url(r'^(?P<order_id>\d+)/finished/$', 'finished'),
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from order.models import Order, OrderDetail
from address.models import Address
from django.template import RequestContext
import datetime
from cart.views import getCart, cleanCart


@login_required
def order(request):
    cart=getCart(request)
    user=request.user
    item_set=cart.cartitem_set.all()
    try:
        address=Address.objects.filter(user=user,
            pk=request.GET['address_id'])[0]
    except:
        address=Address.objects.filter(user=user)[0]
    if item_set.count()>0:
        price=0
        order=Order.objects.create(user=user, address=address, price=price)
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
