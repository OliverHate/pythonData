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
        self.url_template = "https://market.douban.com/book/?type=topic&page={}"
        reg = '<a href="(.*?)".*?<h3>(.*?)</h3>'
        self.reg = re.compile(reg, re.S)

    def getSourceCode(self, url):
        req = urllib2.Request(url=url)
        res = urllib2.urlopen(req)
        source_code = res.read()
        tag = '<a class="hover" id="readbook_tab">书单</a>'
        start = source_code.find(tag)
        source_code = source_code[start:]
        return source_code

    def getBookListUrl(self, source_code):
        book_url = self.reg.findall(source_code)
        for i in xrange(len(book_url)):
            book_url[i] = list(book_url[i])
            book_url[i][0] = "https://market.douban.com{}".format(book_url[i][0])
        return book_url

    def saveTxt(self, book_url):
        with open(r'..\data\bookUrl.txt', 'a') as f:
            for i in book_url:
                f.write("{};{}\n".format(i[0], i[1]))
            print '书单写入完毕'

    def main(self):
        for num in [1, 2, 3]:
            self.url = self.url_template.format(num)
            source_code = self.getSourceCode(self.url)
            book_url = self.getBookListUrl(source_code)
            self.saveTxt(book_url)


class douBanBook():
    def __init__(self):
        self.url = 'https://market.douban.com/book/special/dushuzhou/'
        reg = '"is_debut":false,"title":"(.*?)",.*?","subject_id":"(.*?)",'
        self.reg = re.compile(reg)
        self.pdb = pdb.connect(host='localhost', user='root', passwd='123456', db='douban', charset='utf8')
        self.cur = self.pdb.cursor()
        self.insert_sql = 'insert into douban.douban_catalog(name,num,url) values ("%s","%s","%s")'
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS douban_catalog(
        id int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
        name varchar(80),
        num VARCHAR(30),
        url VARCHAR(100))
        """
        self.cur.execute(create_table_sql)

    def getSourceCode(self, url):
        req = urllib2.Request(url=url)
        res = urllib2.urlopen(req)
        source_code = res.read()
        tag = "'is_mobile': false,"
        start = source_code.find(tag)
        source_code = source_code[start:]
        return source_code

    def getList(self, source_code):
        bookList = self.reg.findall(source_code)
        for num in xrange(len(bookList)):
            bookList[num] = list(bookList[num])
            bookList[num].append("https://book.douban.com/subject/{}/".format(bookList[num][1]))
        return bookList

    def getBookUrlList(self):
        with open('../data/bookUrl.txt', 'r') as f:
            book_url_list = f.read()
            book_url_list = book_url_list.split('\n')
            book_url_list = book_url_list[:-1]
        for num in range(len(book_url_list)):
            book_url_list[num] = book_url_list[num].split(';')[0]
        return book_url_list

    def saveSql(self, book_list):
        for i in book_list:
            insert_sql = self.insert_sql % (i[0], i[1], i[2])
            print insert_sql
            suc = self.cur.execute(insert_sql)
            print suc

    def main(self):
        book_url_list = self.getBookUrlList()
        for url in book_url_list:
            source_code = self.getSourceCode(url)
            book_list = self.getList(source_code)
            self.saveSql(book_list)
        self.pdb.commit()
        self.cur.close()
        self.pdb.close()


def BookListMain():
    douban = DouBanBookList()
    douban.main()


def BookMain():
    book = douBanBook()
    book.main()


if __name__ == '__main__':
    BookListMain()
    BookMain()
