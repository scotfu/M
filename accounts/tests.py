#! /usr/bin/env python
#coding=utf-8

from django.test.client import Client
import unittest
from django.contrib.auth.models import User


class SimpleTest(unittest.TestCase):

    def setUp(self):
        self.client=Client()

    def test_register(self):
        response=self.client.post('/accounts/register/', {'username': 'test',
                  'password': 'testtest',
                  'confirm_password': 'testtest',
                  'email': 'test1@test.com', 'nickname': 'testnick'})

        self.assertTrue(User.objects.all()[0].username=='test')

    def test_login(self):
        User.objects.create_user(username='test', password='testtest')
        response=self.client.post('/accounts/login/', {'username': 'test',
                                  'password': 'testtest'})
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_quicklogin(self):
        response=self.client.post('/accounts/quicklogin/', {'username': 'test',
                                   'password': 'testtest'})
        self.assertTrue('_auth_user_id' in self.client.session)
