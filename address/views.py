#! /usr/bin/env python
#coding=utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.forms import AddressForm
from address.models import Address
from django.template import RequestContext
from django.views.generic import ListView


@csrf_protect
@login_required
def save(request, address_id=None):
    user=request.user
    if request.method =='POST':
        form=AddressForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['address_id']:
                address=Address.objects.get(pk=form.cleaned_data['address_id'])
            else:
                address=Address()
            address.name=form.cleaned_data['name']
            address.address=form.cleaned_data['address']
            address.postal_code=form.cleaned_data['postal_code']
            address.user=user
            address.save()
            return HttpResponseRedirect('/address/')
    else:
        if address_id:
            address=Address.objects.get(pk=address_id)
            if address.user==request.user:
                form=AddressForm(initial={'address_id': address.id,
                    'name': address.name, 'address': address.address,
                    'postal_code': address.postal_code})
        else:
            form=AddressForm()
        return render_to_response('address_form.html', {
            'form': form},
             context_instance=RequestContext(request))


class AddressListView(ListView):
    context_object_name="address_list"
    template_name="address_list.html"

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddressListView, self).dispatch(*args, **kwargs)
