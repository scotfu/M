#! /usr/bin/env python
#coding=utf-8
from django.http import HttpResponseRedirect #HttpResponse Http404
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from accounts.forms import RegisterForm, LoginForm, AccountForm
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from cart.models import Cart
from cart.views import getCart, cartMerge


@csrf_protect
def loginview(request):
    if request.method == 'POST':
        form=LoginForm(request.POST)
        session_cart=getCart(request)
        try:
            next= request.POST['next']
        except:
            next='/'
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    user_cart=getCart(request)
                    cartMerge(user_cart, session_cart)
                    request.session['cart']={}
                    return HttpResponseRedirect(next)
    else:
        if '_auth_user_id' in request.session:
            return HttpResponseRedirect('/')
        else:
            form=LoginForm()
            try:
                next= request.GET['next']
            except:
                next='/'
    return render_to_response('login_form.html',
            {'form': form,
            'next': next},
             context_instance=RequestContext(request))


@csrf_protect
def quickloginview(request):
    if request.method == 'POST':
        form=LoginForm(request.POST)
        session_cart=getCart(request)
        try:
            next=request.META.get('HTTP_REFERER', '/')
        except:
            next='/'
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    user_cart=getCart(request)
                    cartMerge(user_cart, session_cart)
                    request.session['cart']={}
                    return HttpResponseRedirect(next)
        else:
            return render_to_response('login_form.html',
                        {'form': form,
                         'next': next},
                         context_instance=RequestContext(request))


def logoutview(request):
    logout(request)
    return HttpResponseRedirect('/')


@csrf_protect
def register(request):
    if  '_auth_user_id' in request.session:
        return HttpResponseRedirect('/')
    if request.method =='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
            email=form.cleaned_data['email'],
            )
            user_profile=user.get_profile()
            user_profile.nickname=form.cleaned_data['nickname']
            user_profile.save()
            Cart.objects.create(user=user)
            return HttpResponseRedirect('/accounts/register/success/')
    else:
        form=RegisterForm()
    return render_to_response('reg_form.html', {
            'form': form},
            context_instance=RequestContext(request),
    )


@login_required
def modifyview(request):
    user=request.user
    if request.method=='POST':
        form=AccountForm(request.POST)
        if form.is_valid():
            password=form.cleaned_data['confirm_password']
            user.set_password(password)
            user_profile= user.get_profile()
            user_profile.nickname=form.cleaned_data['nickname']
            user_profile.save()
            user.save()
            return HttpResponseRedirect('/accounts/')
    else:
        nickname=user.get_profile().nickname
        form=AccountForm(initial={'nickname': nickname})
    return render_to_response('account_modify.html', {
            'form': form},
             context_instance=RequestContext(request),
             )
