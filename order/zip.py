#! /usr/bin/env python
#coding=utf-8
import zipfile
import os,sys

reload(sys) 
sys.setdefaultencoding('utf-8') 

f_zip = zipfile.ZipFile('汉字.rar'.decode('utf-8'), 'w')
f=open(u'第二人生.mp3', 'w')
f.close()
try:
    f_zip.write(u'第二人生.mp3')
except IOError,ValueError:
    pass
f_zip.close()
