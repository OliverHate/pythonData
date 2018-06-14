# -*- coding:utf-8 -*-
"""
@Time       : 9:02
@Author     :邹文涛
@File       :douBanBookTop250.py
"""
import re
import urllib2
import pymysql as pdb


class douBan():
    #定义浏览器表头，定义正则表达式并编译
    #for循环格式化url链接，调用方法
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"
        }
        reg = '<div class="pl2">.*?  <a href="(.*?)" onclick=.*?; title="(.*?)".*? <p class="pl">(.*?)</p>.*? <span class="rating_nums">(.*?)</span>'
        self.reg = re.compile(reg,re.S)
        self.urlTemplet = "https://book.douban.com/top250?start={}"
        self.conn = pdb.connect(host='localhost',user='root',passwd='123456',port=3306,db='douban',charset='utf8')
        self.creataTableSql = """
                CREATE TABLE IF NOT EXISTS book(
                id int(9) PRIMARY KEY NOT NULL AUTO_INCREMENT , 
                bookName VARCHAR(80) NOT NULL ,  
                author VARCHAR(80) NOT NULL ,
                score VARCHAR(10) NOT NULL ,
                money VARCHAR(10),
                url VARCHAR(80))
                """
    def main(self):
        for n in range(0,250,25):
            self.url = self.urlTemplet.format(n)
            self.findList()
    #getHtml()接受URL参数，并且返回字符串类型的网页源代码
    def getHtml(self):
        req = urllib2.Request(self.url,headers=self.headers)
        response = urllib2.urlopen(req)
        html=response.read()
        return html
    #获取url链接，查找网页所需要元素，写入列表
    #outList为输出二维列表。 outList[0]为一维列表，组成为 书籍名，作者，价格，评分，URL
    def findList(self):
        outList = []
        html = self.getHtml()
        outcome = self.reg.findall(html)
        for line in outcome:
            #@bookName:书名
            #@booUrl:书籍链接
            #@score:评分
            #@author:作者
            #@money:价格
            bookName = line[1]
            bookUrl = line[0]
            score = line[-1]
            complilations = line[2].split('/')
            author = complilations[0]
            money = complilations[-1]
            if not (money.find('元')== -1):
                money = money[:-3]
            outList.append((bookName,author,money,score,bookUrl))

        self.saveCsv(outList)
        self.saveSql(outList)
    # saveCsv(）保存文件
    #将参数列表写入文件
    def saveCsv(self,outList):
        with open(r'./BookOut.txt','a') as f:
            for line in outList:
                out = ';'.join(line)
                f.write(out+'\n')
                print out+'写入成功'
    def saveSql(self,outList):
        outList[:][2:4]=outList[:][2:4]
        cursor =self.conn.cursor()
        cursor.execute(self.creataTableSql)
        insertSql = "INSERT INTO book(bookName,author,score,money,url) values ('%s','%s','%s','%s','%s')"
        for rowNum in outList:
            insert = insertSql % rowNum
            print(insert)
            cursor.execute(insert)
        self.conn.commit()

if __name__ == '__main__':
    start = douBan()
    start.main()
