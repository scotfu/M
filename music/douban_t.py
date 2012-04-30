#! /usr/bin/env python
#coding=utf-8
import urllib
import urllib2
import json
import sys
import os
import pprint
import time
test='http://api.douban.com/music/subjects?tag=Pop&&alt=json&start-index=1&max-results=50'
reload(sys)
sys.setdefaultencoding('utf8')

base_url='http://api.douban.com/music/subject/'
comment_url='http://api.douban.com/review/'
search_url=r'http://api.douban.com/music/subjects?'
apikey='?apikey=0aba7aba95bae0ec202f702fc130a2c4'


album_id='10581363'
review_id='5398388'
data_type='&alt=json'
url=base_url+album_id+apikey+data_type
review_url=comment_url+review_id+apikey+data_type
upload_dir=os.path.dirname(__file__).replace('\\', '/')+'/media/upload'

def my_search():
    data=urllib.urlopen('http://api.douban.com/music/subjects?tag=Pop&apikey=0aba7aba95bae0ec202f702fc130a2c4&alt=json&start-index=1&max-results=10')
    json_data=json.load(data)
    pprint.pprint(json_data['entry'])
    for album in json_data['entry']:
        print album['title']['$t'],album['author'][0]['name']['$t']
        #    f=open(r'C:\Users\Scot\Desktop\333.txt')
#    f.close()
#    f=open(r'C:\Users\Scot\Desktop\222.txt', 'w')
#    f.write('1')
#    f.close()


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
    image_name=album_id+'.jpg'
    img_path=upload_dir+'/'+image_name
    open(img_path, 'wb').write(rs)
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
    return genre


def get_comment():
    comment=urllib.urlopen(review_url)
    json_data=json.load(comment)
    return json_data['summary']['$t'].encode('utf-8')


def album_import():
    album=urllib.urlopen(url)
    json_data=json.load(album)
    get_image(json_data)
    title=get_data(json_data, 'title')
    singer=json_data['author'][0]['name']['$t'].encode('utf-8')
    description=get_data(json_data, 'summary')
    image=get_image(json_data)
    year=get_year(json_data)
    genre=get_genre(json_data)
    isbn=get_isbn(json_data)
    company=get_company(json_data)
    new_album=Album.objects.create(title=title, singer=singer, year=year,
            description=description, genre=genre, isbn=isbn, company=company,
            pic=image, price=100, amount=100, store_id=1)
#    comment=get_comment()
my_search()
