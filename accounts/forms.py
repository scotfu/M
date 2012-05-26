#! bin/env python
#coding=utf-8
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms
#from django.forms import ModelForm
import re


class LoginForm(forms.Form):

    username=forms.CharField(max_length=20, label='用户名')
    password=forms.CharField(widget= forms.PasswordInput(), label='密码')

    def clean_username(self):
        username=self.cleaned_data['username']
        return username

    def clean_password(self):
        password=self.cleaned_data['password']
        user = authenticate(username=self.cleaned_data['username'],
        password=self.cleaned_data['password'])
        if user is None:
            raise forms.ValidationError('用户名或者密码错误')
        return password


class RegisterForm(forms.Form):

    email=forms.EmailField(label='Email')
    username=forms.CharField(max_length=20, label='用户名')
    password=forms.CharField(widget=forms.PasswordInput(), label='密码')
    confirm_password=forms.CharField(widget=forms.PasswordInput(),
                            label='确认密码')
    nickname=forms.CharField(max_length=20, label='昵称')

    def clean_username(self):
        username=self.cleaned_data['username']
        if not re.search(r'\w+$', username):
            raise ValidationError('输入非法')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('用户名已被注册')

    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('邮箱地址已被注册')

    def clean_confirm_password(self):
        if 'password' in self.cleaned_data:
            password=self.cleaned_data['password']
            if 'confirm_password' in self.cleaned_data:
                confirm_password=self.cleaned_data['confirm_password']
                if password == confirm_password:
                    return confirm_password
                raise ValidationError('两次输入的密码不一样')
            raise forms.ValidationError('请输入确认密码')
        raise forms.ValidationError('请输入密码')


class CommentForm(forms.Form):
    title=forms.CharField(max_length=20, help_text="")
    content=forms.CharField(max_length=512, help_text="")

    def clean_title(self):
        title=self.cleaned_data['title']
        if title =='':
            raise ValidationError('Can not be null')
        return title

    def clean_content(self):
        content=self.cleaned_data['content']
        if content=='':
            raise ValidationError('Not null')
        return content


class AccountForm(forms.Form):
#    user_id=forms.IntegerField(widget=forms.HiddenInput())
    nickname=forms.CharField(max_length=20, label='昵称')
    password=forms.CharField(widget=forms.PasswordInput(), label='密码')
    confirm_password=forms.CharField(widget=forms.PasswordInput(),
                label='确认密码')

    def clean_confirm_password(self):
        if 'password' in self.cleaned_data:
            password=self.cleaned_data['password']
            if 'confirm_password' in self.cleaned_data:
                confirm_password=self.cleaned_data['confirm_password']
                if password==confirm_password:
                    return confirm_password
                raise forms.ValidationError('Do not match')
            raise forms.ValidationError('Type the confirm password')
        raise forms.ValidationError('Type the password')


class AddressForm(forms.Form):
    address_id=forms.IntegerField(required=False, label='id',
        widget=forms.HiddenInput())
    name=forms.CharField(max_length=20, label='姓名')
    address=forms.CharField(max_length=512, label='地址')
    postal_code=forms.CharField(max_length=20, label='邮编')

    def clean_id(self):
        pass

    def clean_name(self):
        return self.cleaned_data['name']

    def clean_address(self):
        return self.cleaned_data['address']

    def clean_postal_code(self):
        return self.cleaned_data['postal_code']


class AlbumForm(forms.Form):

    def clean_title(self):
        title=self.cleaned_data['title']
        if title=='':
            raise ValidationError('Not null')
        return title

    def clean_price(self):
        price=self.cleaned_data['price']
        return price

    def clean_amount(self):
        amount=self.cleaned_data['amount']
        return amount

    def clean_year(self):
        year=self.cleaned_data['year']
        return year

    def clean_isbn(self):
        isbn=self.cleaned_data['isbn']
        return isbn

    def clean_company(self):
        company=self.cleaned_data['company']
        return company

    def clean_genre(self):
        genre=self.cleaned_data['genre']
        return genre

    def clean_store(self):
        store=self.cleaned_data['store']
        return store
