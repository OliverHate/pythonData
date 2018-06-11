# -*- coding:utf-8 -*-
"""
@Time       : 8:30
@Author     :邹文涛
@File       :DowIp.py
"""
import urllib2
from bs4 import BeautifulSoup
from pandas import DataFrame
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class DowIP():
    def __init__(self,num):#类初始化方法
        self.IpUrl = 'http://www.xicidaili.com/nn/{}'.format(num) #网页地址

    def GetHtml(num,IpUrl):
        headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'}
        requests =  urllib2.Request(IpUrl,headers=headers)
        html = urllib2.urlopen(requests).read()
        return html


    def findIp(self,html):
        ipList = []
        bsobj = BeautifulSoup(html,'html.parser')
        ipBlock = bsobj.find_all('tr') #查找tr结构
        ipBlock = ipBlock[1:]#去除表格头部信息
        for ipParagraph in ipBlock:
            tdLine = ipParagraph.find_all('td') #代码分块查找， 即取出表列按条信息
            IPAddree = tdLine[1].string+":"+tdLine[2].string #获取IP以及端口，并组合
            try:  #服务器地址存在出错可能性，进行错误截取
                address = tdLine[3].find('a').get_text() #获取服务器地址
            except AttributeError as e :
                print '获取出错'
                address = '日照'
            genre = tdLine[5].string
            ipList.append([IPAddree,genre,address])
            print "获取IP地址为:"+IPAddree #输出反馈信息
        self.saveIp(ipList)

    def saveIp(slef,ipList):
        columns = ['IP','服务器地址','类型']
        ipDf = DataFrame(data=ipList,columns=columns)
        ipDf.to_csv(path_or_buf=r'./src/IP.csv', index=False, header=False, mode='a+', encoding='utf-8')

if __name__ == '__main__':

    for num in range(2, 1000):
        time.sleep(2)
        IP = DowIP(num)
        html = IP.GetHtml(IP.IpUrl)  # 调用方法，进行网页源代码获取
        IP.findIp(html)  # 解析源代码，获取所需要的数据


# ipUrl = 'http://www.xicidaili.com/nn/2'
# headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'}
# requests =  urllib2.Request(ipUrl,headers=headers)
# html = urllib2.urlopen(requests).read()
# bsobj = BeautifulSoup(html,'html.parser')
# ipBlock = bsobj.find_all('tr')
# ipBlock = ipBlock[1:]
# ipPage = []
# for ipParagraph in ipBlock:
#     tdLine = ipParagraph.find_all('td')
#     IPAddree = tdLine[1].string+":"+tdLine[2].string #获取IP以及端口，并组合
#     address = tdLine[3].find('a').get_text() #获取服务器地址
#     genre = tdLine[5].string
#     ipPage.append([IPAddree,genre,address])
#
# columns = ['IP','服务器地址','类型']
# ipDf = DataFrame(data=ipPage,columns=columns)
#
# print ipDf.head()
# ipDf.to_csv(path_or_buf=r'./src/IP.csv',index=False,header=False,mode='a+',encoding='utf-8')



