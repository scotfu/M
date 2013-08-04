#! /usr/bin/env python
#coding=utf-8
import urllib2

re = urllib2.Request(r'http://img1.douban.com/lpic/s9033740.jpg')  
rs = urllib2.urlopen(re).read()  
open('C:/django_1/music/music/media/upload/10581362.jpg', 'wb').write(rs)  

