# -*- coding:utf-8 -*-
"""
@Time       :2018/6/11 10:37
@Author     :邹文涛
@File       :douBanBookList.py
@Software: PyCharm
"""

import urllib2
import re
import pymysql as pdb

class DouBanBookList():
    def __init__(self):
        self.url = "https://market.douban.com/book/?type=topic&page={}"
        reg = '<a href="(.*?)" target="_blank".*?class="special-item">.*?<h3>(.*?)</h3>'
        self.reg = re.compile(reg, re.S)

    def getSourceCode(self,url):
        req = urllib2.Request(url=url)
        res = urllib2.urlopen(req)
        source_code = res.read()
        tag = '<a class="hover" id="readbook_tab">书单</a>'
        start = source_code.find(tag)
        source_code = source_code[start:]
        return source_code

    def getBookListUrl(self):
        source_code = self.getSourceCode('https://market.douban.com/book/?type=topic&page=1')
        tag = '<a class="hover" id="readbook_tab">书单</a>'
        start = source_code.find(tag)
        source_code = source_code[start:]
        book_url = self.reg.findall(source_code)
        for i in xrange(len(book_url)):
            book_url[i] = list(book_url[i])
            book_url[i][0] = "https://market.douban.com{}".format(book_url[i][0])
        return book_url

    def saveTxt(self,book_url):
        with open(r'..\data\bookUrl.txt','a') as f:
            for i in book_url:
                f.write("{}:{}\n".format(i[0],i[1]))
            print 'over'

    def saveSql(self):
        pass

def main():
    douban = DouBanBookList()
    book_url = douban.getBookListUrl()
    douban.saveTxt(book_url)


if __name__ == '__main__':
    main()