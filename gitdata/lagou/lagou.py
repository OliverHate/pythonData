# -*- coding:utf-8 -*-
"""
@Time       : 8:47
@Author     :邹文涛
@File       :lagou.py
"""
import requests
import time
import random
from pandas import DataFrame
import sys
import numpy
class lagou:
    def __init__(self,occupation):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.data=[]
        self.occupation = occupation
        self.api = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'
        self.header = {'Accept':'application/json, text/javascript, */*; q=0.01',
           'Accept-Encoding':'gzip, deflate, br',
           'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
           'Cache-Control':'max-age=0',
           'Connection':'keep-alive',
           'Content-Length':'25',
           'Content-Type':	'application/x-www-form-urlencoded; charset=UTF-8',
           'Host':	'www.lagou.com',
           'Referer':'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0',
           'X-Anit-Forge-Code':'0',
           'X-Anit-Forge-Token':'None',
           'X-Requested-With':'XMLHttpRequest'
           }
        self.proxyIpList = []
        ipList = open(r'.\src\IP\Ip.txt','r').read()
        for ip in ipList:
            self.proxyIpList.append('http://'+ip)
        self.pushParameter = {'first':'flase',  'kd':occupation,}
    def getHtml(self,page):
        self.pushParameter['pn'] = page
        proxies = self.getProxyIp()
        try:
            html = requests.post(self.api, data=self.pushParameter, headers=self.header, proxies=proxies)
            print '成功'
        except requests.exceptions.ProxyError as e :
            time.sleep(5)
            self.getHtml(self,page)
            print '无法使用代理IP'
            pass #无法使用代理IP
        except requests.exceptions.ConnectionError as e:
            print '连接超时'
            pass #连接超时
        try:
            jsonHtml = html.json()['content']['positionResult']['result']
            for num in range(15):
                b = jsonHtml[num]
                self.data.append([b['positionName'], b['workYear'], b['education'], b['jobNature'], b['financeStage'] \
                                     , b['city'], b['salary'], ';'.join(b['companyLabelList']), b['companyFullName']])
            df = DataFrame(data=self.data)
            df.to_csv(path_or_buf=r'./src/python.csv', index=False, header=False, mode='a+')
        except KeyError as e:
            print html.json()
            print '出错'


    def getProxyIp(self):
        proxyIp = random.choice(self.proxyIpList)
        proxies = {'http':proxyIp}
        return proxies



if __name__ == '__main__':
    a = lagou('python')
    for i in range(1,31):
        a.getHtml(str(i))