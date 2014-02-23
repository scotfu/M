#! /usr/bin/env python
#coding=utf-8

import urllib
import urllib2
import json
import sys
import os
import time
import logging
reload(sys)
sys.setdefaultencoding('utf8')

sys.path.append('/home/fu/workspaces/M/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.local'
from django.conf import settings

from album.models import Album, Genre
base_url = r'http://api.douban.com/music/subject/'
comment_url = r'http://api.douban.com/review/'
search_url = r'http://api.douban.com/music/subjects'
apikey = 'apikey=' + os.environ['DOUBAN_API_KEY']
default_data_type = 'alt=json'

upload_dir = os.path.dirname(__file__).replace('\\', '/')+'../media/upload'
log_dir = os.path.dirname(__file__).replace('\\', '/') + '../logs'


def initlog():
    logger = logging.getLogger()
    logfile = 'douban.log'
    hdlr = logging.FileHandler(log_dir+'/douban_log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)
    return logger
mylogging=initlog()


def basesearch(s_type, word, start=1, length=50):
    data=urllib.urlopen(search_url+'?'+s_type+'='+word+'&'+apikey
                          +'&'+default_data_type
                          +'&start-index='+str(start)
                          +'&max-results='+str(length))
    print search_url+'?'+s_type+'='+word+'&'+apikey+'&'+default_data_type+'&start-index='+str(start) +'&max-results='+str(length)

    json_data=json.load(data)
    mylogging.info('读取搜索结果成功')
    for album in json_data['entry']:
        try:
            Album.objects.get(title=album['title']['$t'],
                              singer=album['author'][0]['name']['$t'])
            mylogging.info(album['title']['$t']+'已有该专辑')
        except:
            try:
                album_import(album['id']['$t']+'?'+apikey+'&'
                                   +default_data_type)
                logging.info(album['title']['$t']+'添加成功')
                time.sleep(0.5)
            except:
                mylogging.info(album['id']['$t']+': '+album['title']['$t']
                               +'添加失败')
                print sys.exc_info()[0], sys.exc_info()[1]


def search_by_key_word(key_word='Pop', start=1, result_length=50):
    basesearch(s_type='q', word=key_word, start=start, length=result_length)


def search_by_tag(tag='Pop', start=1, result_length=50):
    basesearch(s_type='tag', word=tag, start=start, length=result_length)


def get_from_db_attribute(json_data, name):
    attributes=json_data['db:attribute']
    for attribute in attributes:
        if attribute['@name']==name:
            mylogging.info(name+'已得到')
            return attribute['$t'].encode('utf-8')


def get_data(json_data, attribute):
    mylogging.info(attribute+'已得到')
    return json_data[attribute]['$t'].encode('utf-8')


def downImage(url):
    re = urllib2.Request(url)
    rs = urllib2.urlopen(re).read()
    ISOTIMEFORMAT='%Y%m%d%H%M%S'
    image_name=str(time.time())+'.jpg'
    img_path=upload_dir+'/'+image_name
    open(img_path, 'wb').write(rs)
    mylogging.info(image_name+'封面下载成功')
    return 'upload/'+image_name


def get_image(json_data):
    links=json_data['link']
    for link in links:
        if link['@rel']=='image':
            image_url=link['@href'].encode('utf-8').replace('spic', 'lpic')
            return downImage(image_url)


def get_year(json_data):
    return int(get_from_db_attribute(json_data, 'pubdate')[0:4])


def get_isbn(json_data):
    return get_from_db_attribute(json_data, 'ean')


def get_company(json_data):
    return get_from_db_attribute(json_data, 'publisher')


def get_genre(json_data):
    dbtag=json_data['db:tag']
    name=dbtag[-1]['@name'].encode('utf-8')
    genre=Genre.objects.get_or_create(name=name)[0]
    mylogging.info(genre.name+'曲风获得成功')
    return genre


#def get_comment():
#    comment=urllib.urlopen(review_url)
#    json_data=json.load(comment)
#    return json_data['summary']['$t'].encode('utf-8')


def album_import(url):
    album=urllib.urlopen(url)
    json_data=json.load(album)
    title=get_data(json_data, 'title')
    singer=json_data['author'][0]['name']['$t'].encode('utf-8')
    description=get_data(json_data, 'summary').replace('\n', '<br>')
    year=get_year(json_data)
    genre=get_genre(json_data)
    isbn=get_isbn(json_data)
    company=get_company(json_data)
    image=get_image(json_data)
    mylogging.info('开始添加')
    new_album=Album.objects.create(title=title, singer=singer, year=year,
            description=description, genre=genre, isbn=isbn, company=company,
            pic=image, price=100, amount=100, store_id=1)


if __name__ == '__main__':
    search_by_key_word()
