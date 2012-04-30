#! /usr/bin/env python
#coding=utf-8
import urllib
import urllib2
import json
from album.models import Album, Genre
import sys
import os
import time
reload(sys)
sys.setdefaultencoding('utf8')

base_url='http://api.douban.com/music/subject/'
comment_url='http://api.douban.com/review/'
search_url=r'http://api.douban.com/music/subjects?'
apikey='?apikey=0aba7aba95bae0ec202f702fc130a2c4'


album_id='10581363'
review_id='5398388'
data_type='&alt=json'
#url=base_url+album_id+apikey+data_type
review_url=comment_url+review_id+apikey+data_type
upload_dir=os.path.dirname(__file__).replace('\\', '/')+'/media/upload'

def my_search(tag='Pop',start=1, end=50):
    data=urllib.urlopen('http://api.douban.com/music/subjects?tag='+tag+'+&apikey=0aba7aba95bae0ec202f702fc130a2c4'
                         +data_type+'&start-index='+str(start)+'&max-results='+str(end))
    json_data=json.load(data)
    print 'loading douban data \n'
    for album in json_data['entry']:
        try:
            Album.objects.get(title=album['title']['$t'],singer=album['author'][0]['name']['$t'])
        except:
            try:
                album_import(album['id']['$t']+apikey+data_type)
                print album['id']['$t']+' Successed\n'
                time.sleep(0.5)
            except:
                pass


def get_from_db_attribute(json_data, name):
    attributes=json_data['db:attribute']
    for attribute in attributes:
        if attribute['@name']==name:
            return attribute['$t'].encode('utf-8')


def get_data(json_data, attribute):
    return json_data[attribute]['$t'].encode('utf-8')


def downImage(url):
    re = urllib2.Request(url)
    rs = urllib2.urlopen(re).read()
    ISOTIMEFORMAT='%Y%m%d%H%M%S'
    image_name=str(time.strftime(ISOTIMEFORMAT))+'.jpg'
    img_path=upload_dir+'/'+image_name
    open(img_path, 'wb').write(rs)
    print 'image successed\n'
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
    print 'genre successed\n'
    return genre


def get_comment():
    comment=urllib.urlopen(review_url)
    json_data=json.load(comment)
    return json_data['summary']['$t'].encode('utf-8')


def album_import(url):
    album=urllib.urlopen(url)
    json_data=json.load(album)
    title=get_data(json_data, 'title')
    singer=json_data['author'][0]['name']['$t'].encode('utf-8')
    description=get_data(json_data, 'summary').replace(r'\n','<br>')
    image=get_image(json_data)
    year=get_year(json_data)
    genre=get_genre(json_data)
    isbn=get_isbn(json_data)
    company=get_company(json_data)
    new_album=Album.objects.create(title=title, singer=singer, year=year,
            description=description, genre=genre, isbn=isbn, company=company,
            pic=image, price=100, amount=100, store_id=1)
#    comment=get_comment()

