# -*- coding:utf-8 -*-
"""
@Time       : 13:56
@Author     :邹文涛
@File       :sina.py
"""

import urllib2
import json
import pymysql as mdb
import csv
import sys
import time


class sina():
    def __init__(self):
        self.data = []

    def getHtml(self,url):
        url = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=164&lid=1693&num=50&page=1'
        req = urllib2.Request(url)
        html = urllib2.urlopen(req).read()
        return html
    def getData(self):
        def extract(line):
            print line
            print '-----'

        html = self.getHtml('s')
        hjson = json.loads(html)
        newList = hjson['result']['data']
        currenTime = time.time()
        currenTime = int(currenTime)


        for line in newList:
            date = line['ctime']
            date = int(date)
            if (currenTime - date) <= 86400:
                source =line['source']
                intro = line['intro']
                keywords = line['keywords']
                title = line['title']
                titleUrl = line['url']
                wapUrl = line['wapurl']
                date = time.strftime('%Y-%m-%d %H:%M', time.localtime(date))
                print keywords, title,source,date, titleUrl, wapUrl, intro

    def createCsv(self,category):
        category ='财经滚动'
        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        fileName = '.\data\{}\{}.csv'
        fileName = fileName.format(category,date)
        print fileName


if __name__ == '__main__':
    url = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=164&lid=1693&num=50&page=1'
    star = sina()
    star.getData()
    # urls = {'财经滚动':'http://feed.mix.sina.com.cn/api/roll/get?pageid=164&lid=1693&num=50&page=1',
    #         '公司新闻': 'http://feed.mix.sina.com.cn/api/roll/get?pageid=164&lid=1694&num=50&page=1',
    #         '产业新闻': 'http://feed.mix.sina.com.cn/api/roll/get?pageid=164&lid=1695&num=50&page=1',
    #         '深度报道': 'http://feed.mix.sina.com.cn/api/roll/get?pageid=164&lid=1696&num=50&page=1',
    #         '人事变动': 'http://feed.mix.sina.com.cn/api/roll/get?pageid=164&lid=1697&num=50&page=1'}

