#encoding:utf-8
from __future__ import unicode_literals
import sys
import os

sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(__file__)),'dnovel'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'dnovel.settings'
os.environ['SCRAPY_SETTINGS_MODULE']='settings'
from lost import Lost
import logging
from scrapy.settings import Settings
from novel.models import Novel
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings


__author__ = 'meng'

def setup_crawler(book = None,config = None,url = None):
    if not book and not config and not url:
        print "至少输入其中两项"
        return
    if book:
        try:
            novel = Novel.objects.get(name = book)
        except:
            novel = None
    else:
        novel = None
    if novel:
        start_url = novel.start_url
        spider = Lost(start_urls = [start_url],book = novel,config = novel.spider_class)
        #crawler = Crawler(Settings(dict(ITEM_PIPELINES='spider.pipelines.CollectionPipeline')))
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
        log.start(loglevel=logging.DEBUG)
        reactor.run()
    else:
        if config and url:
            start_url = url
            spider = Lost(start_urls = [start_url],bookname = book,config = config,url = url)
            #crawler = Crawler(Settings(dict(ITEM_PIPELINES='spider.pipelines.CollectionPipeline')))
            settings = get_project_settings()
            crawler = Crawler(settings)
            crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
            crawler.configure()
            crawler.crawl(spider)
            crawler.start()
            log.start(loglevel=logging.DEBUG)
            reactor.run()
if  __name__ == "__main__":
    #setup_crawler('宝鉴',config='fftxt',url='http://www.fftxt.net/book/2982/')
    #setup_crawler('魔天记',config='siluke',url='http://www.siluke.com/0/96/96956/')
    setup_crawler('莽荒纪',config='biquge',url='http://www.biquge.com/0_45/')
    #setup_crawler('海上长城',config='fftxt',url='http://www.fftxt.net/book/4837/')
    #print sys.path
    #settings = get_project_settings()
    #print settings['DEBUG']