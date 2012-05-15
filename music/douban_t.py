#! /usr/bin/env python
#coding=utf-8
import urllib
import urllib2
import json
import sys
import os
import pprint
import logging
import time
reload(sys)
sys.setdefaultencoding('utf8')

base_url=r'http://api.douban.com/music/subject/'
comment_url=r'http://api.douban.com/review/'
search_url=r'http://api.douban.com/music/subjects?q='
apikey='apikey=0aba7aba95bae0ec202f702fc130a2c4'
default_data_type='alt=json'

upload_dir=os.path.dirname(__file__).replace('\\', '/')+'/media/upload'

log_dir=os.path.dirname(__file__).replace('\\', '/')

def initlog():
 # 生成一个日志对象
    logger = logging.getLogger()
    # 生成一个Handler。logging支持许多Handler，
    # 象FileHandler, SocketHandler, SMTPHandler等，我由于要写
    # 文件就使用了FileHandler。
    # logfile是一个全局变量，它就是一个文件名，如：'crawl.log'
    logfile = 'douban.log'
    hdlr = logging.FileHandler(log_dir+'/log.txt')
    # 成一个格式器，用于规范日志的输出格式。如果没有这行代码，那么缺省的
    # 格式就是："%(message)s"。也就是写日志时，信息是什么日志中就是什么，
    # 没有日期，没有信息级别等信息。logging支持许多种替换值，详细请看
    # Formatter的文档说明。这里有三项：时间，信息级别，日志信息
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    # 将格式器设置到处理器上
    hdlr.setFormatter(formatter)
    # 将处理器加到日志对象上
    logger.addHandler(hdlr)
    # 设置日志信息输出的级别。logging提供多种级别的日志信息，如：NOTSET, 
    # DEBUG, INFO, WARNING, ERROR, CRITICAL等。每个级别都对应一个数值。
    # 如果不执行此句，缺省为30(WARNING)。可以执行：logging.getLevelName
    # (logger.getEffectiveLevel())来查看缺省的日志级别。日志对象对于不同
    # 的级别信息提供不同的函数进行输出，如：info(), error(), debug()等。当
    # 写入日志时，小于指定级别的信息将被忽略。因此为了输出想要的日志级别一定
    # 要设置好此参数。这里我设为NOTSET（值为0），也就是想输出所有信息
    logger.setLevel(logging.NOTSET)
    return logger

logging=initlog()


def my_search(key_word='Pop',start=1, end=50):
    data=urllib.urlopen(search_url+key_word+'&'+apikey+'&'+data_type+'&start-index='+str(start)+'&max-results='+str(end))
    json_data=json.load(data)
    logging.info('读取搜索数据成功')
    for album in json_data['entry']:
        try:
            Album.objects.get(title=album['title']['$t'],singer=album['author'][0]['name']['$t'])
            logging.info('已有该专辑')
        except:
            try:
                album_import(album['id']['$t']+apikey+data_type)
                logging.info(album['id']['$t']+'添加成功')
                time.sleep(0.5)
            except:
                logging.error(album['id']['$t']+'添加失败')


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
    logging.info(image_name+'专辑封面下载成功')
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
    logging.info(genre+'添加曲风成功')
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
    description=get_data(json_data, 'summary').replace('\n','<br>')
    image=get_image(json_data)
    year=get_year(json_data)
    genre=get_genre(json_data)
    isbn=get_isbn(json_data)
    company=get_company(json_data)
    new_album=Album.objects.create(title=title, singer=singer, year=year,
            description=description, genre=genre, isbn=isbn, company=company,
            pic=image, price=100, amount=100, store_id=1)
    



