# -*- coding:utf-8 -*-
"""
@Time       : 9:45
@Author     :邹文涛
@File       :main.py
# mapff= list(map(lambda m:html.json()['content']['positionResult']['result'][0]['industryField'],range(15)))
"""
import requests
import re
import time
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import jieba
from wordcloud import  WordCloud
import matplotlib as mpl
from pyecharts import Geo
from pandas import read_csv
from pandas import DataFrame,Series
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'
data = []
header = {'Accept':'application/json, text/javascript, */*; q=0.01',
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
ipList = ['117.69.230.31:3852',
'122.236.213.104:2314',
'202.101.248.42:6879',
'218.91.224.229:2137',
'175.174.5.64:2314',
'113.236.32.6:8946',
'119.85.13.90:2765',
'182.42.157.9:6856',
'124.224.186.170:6487',
'113.236.34.136:8946',
'114.99.15.205:6890',
'27.28.232.120:7838',
'117.87.72.62:2315',
'119.85.3.9:2765',
'42.229.185.108:2589',
'49.84.122.103:2646',
'117.23.33.25:2319',
'114.235.46.22:3278',
'220.178.156.16:7541',
'42.85.25.36:2314']
# proxyIpList = ['http://14.211.116.16:9999',
# 'http://218.20.218.28:8118',
# 'http://221.231.109.40:3128',
# 'http://221.10.159.234:1337',
# 'http://106.42.96.103:808',
# 'http://118.114.77.47:8080',
# 'http://125.106.225.226:808',
# 'http://110.73.7.229:8123']
proxyIpList = []
for ipLine in ipList:
    proxyIpList.append('http://'+ipLine)
for n in range(30):
    time.sleep(4)
    proxyIp = random.choice(proxyIpList)
    proxies = {'http':proxyIp}
    pn = {'first':'true',
           'kd':'PHP',
           'pn':str(n)}
    try:
        html = requests.post(url,data=pn,headers=header,proxies = proxies)
    except requests.exceptions.ProxyError as e:
        print '代理失效'
        proxyIp = random.choice(proxyIpList)
        proxies = {'http': proxyIp}
        html = requests.post(url, data=pn, headers=header, proxies=proxies)
    except requests.exceptions.ConnectionError as e:
        print '超时'
        proxyIp = random.choice(proxyIpList)
        proxies = {'http': proxyIp}
        html = requests.post(url, data=pn, headers=header, proxies=proxies)
    try:
        a = html.json()['content']['positionResult']['result']
    except KeyError as e:
        print html.json()
        print '出错'
        continue

    for num in range(15):
        b = a[num]
        data.append([b['positionName'],b['workYear'],b['education'],b['jobNature'],b['financeStage'] \
                        ,b['city'] ,b['salary'],';'.join(b['companyLabelList']),b['companyFullName']])
    df = DataFrame(data=data)
    df.to_csv(path_or_buf=r'./src/PHP.csv', index=False,header=False, mode='a+')
    print '写入一次完成'
"""
positionName:岗位职称
workYear:1-3年
education:学历要求
jobNature:工作类型 （全职与兼职）
financeStage:公司发展（融资形式）
city: 工作地点（城市）
salary:工资
companyLabelList:工作福利（为列表，需处理）
companyFullName:公司名称

positionLables:有关标签（为列表，需处理）

"""


# print a['education']
# print a['city']
# print a['salary']
# print a['positionName']
# print a['companyFullName']
# print ';'.join(a['positionLables'])
#
# columns = ['岗位职称','工作经验','学历要求','工作类型','公司发展','工作地点','工资','工作福利','公司名称']
# df = DataFrame(data = data)
# df.to_csv(path_or_buf=r'./src/Python.csv',index=False,mode='a+')

