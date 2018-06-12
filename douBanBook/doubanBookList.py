# -*- coding:utf-8 -*-
"""
@Time       :2018/6/12 10:58
@Author     :邹文涛
@File       :doubanBookList.py
@Software: PyCharm
"""
# 程序实现爬取豆瓣推荐书单并将保存数据库
# DouBanBookList 爬取推荐书单链接，并以 链接；书单名 格式保存txt 文件名为BookUrl.txt
# DouBanBook 读取文件 并保存书单内书本的链接。写入数据库 （需创建douban数据库），修改数据库配置
import urllib2
import re
import pymysql as pdb

class DouBanBookList():
    def __init__(self):
        self.url_template = "https://market.douban.com/book/?type=topic&page={}"
        reg = '<a href="(.*?)".*?<h3>(.*?)</h3>'
        self.reg = re.compile(reg, re.S)

    #getSourceCode() 以url为参数，返回源代码（截取部分，方便正则匹配）
    def getSourceCode(self, url):
        req = urllib2.Request(url=url)
        res = urllib2.urlopen(req)
        source_code = res.read()
        tag = '<a class="hover" id="readbook_tab">书单</a>'
        start = source_code.find(tag)
        source_code = source_code[start:]
        return source_code

    #getBookListUrl() 接受源代码，匹配其中的书单链接并格式化连接， 返回二维数组 格式为 [[url],[name]]
    def getBookListUrl(self, source_code):
        book_url = self.reg.findall(source_code)
        for i in xrange(len(book_url)):
            book_url[i] = list(book_url[i])
            book_url[i][0] = "https://market.douban.com{}".format(book_url[i][0])
        return book_url

    #saveTxt() 接受二维数组，写入bookUrl.txt文件内
    def saveTxt(self, book_url):
        with open(r'..\data\bookUrl.txt', 'a') as f:
            for i in book_url:
                f.write("{};{}\n".format(i[0], i[1]))
            print '书单写入完毕'

    #程序入口
    def main(self):
        for num in [1, 2, 3]:
            self.url = self.url_template.format(num)
            source_code = self.getSourceCode(self.url)
            book_url = self.getBookListUrl(source_code)
            self.saveTxt(book_url)

#doubanBook
class douBanBook():
    def __init__(self):
        self.url = 'https://market.douban.com/book/special/dushuzhou/'
        reg = '"is_debut":false,"title":"(.*?)",.*?","subject_id":"(.*?)",'
        self.reg = re.compile(reg)
        # 创建看数据库连接
        # host:IP地址
        # user:数据库用户名
        # passwd:用户密码
        # db：数据库
        # charset:字符编码
        self.pdb = pdb.connect(host='localhost', user='root', passwd='123456', db='douban', charset='utf8')
        self.cur = self.pdb.cursor()
        #insert语句模版，接受参数进行格式化
        self.insert_sql = 'insert into douban.douban_catalog(name,num,url) values ("%s","%s","%s")'
        #创建数据表语句
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS douban_catalog(
        id int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
        name varchar(80),
        num VARCHAR(30),
        url VARCHAR(100))
        """
        self.cur.execute(create_table_sql)

    # 读取文件，获取书单链接
    def getBookUrlList(self):
        with open('../data/bookUrl.txt', 'r') as f:
            book_url_list = f.read()
            book_url_list = book_url_list.split('\n')
            book_url_list = book_url_list[:-1]
        for num in range(len(book_url_list)):
            book_url_list[num] = book_url_list[num].split(';')[0]
        return book_url_list

    #获取源代码，返回部分截取源代码
    def getSourceCode(self, url):
        req = urllib2.Request(url=url)
        res = urllib2.urlopen(req)
        source_code = res.read()
        tag = "'is_mobile': false,"
        start = source_code.find(tag)
        source_code = source_code[start:]
        return source_code

    #得到 书名，编号，链接，三维数组
    def getList(self, source_code):
        bookList = self.reg.findall(source_code)
        for num in xrange(len(bookList)):
            bookList[num] = list(bookList[num])
            bookList[num].append("https://book.douban.com/subject/{}/".format(bookList[num][1]))
        return bookList

    #根据书名编号链接 写入数据库
    def saveSql(self, book_list):
        for i in book_list:
            insert_sql = self.insert_sql % (i[0], i[1], i[2])
            print insert_sql
            suc = self.cur.execute(insert_sql)
            print suc

    #程序入口
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
