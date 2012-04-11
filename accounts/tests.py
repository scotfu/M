#! /usr/bin/env python
#coding=utf-8

from django.test.client import Client
import unittest


class SimpleTest(unittest.TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def setUp(self):
        self.client=Client()

    def test_detail(self):
        response=self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)