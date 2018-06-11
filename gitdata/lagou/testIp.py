# -*- coding:utf-8 -*-
"""
@Time       : 10:45
@Author     :邹文涛
@File       :testIp.py
"""
import requests
from pandas import read_csv
from pandas import DataFrame
import random
import re
import threading
import time
def getIP():
    columns = ['IP','类型','服务器地址']
    df = read_csv(filepath_or_buffer=r'.\src\IP.csv',names=columns)
    df =  df[df['类型']=='HTTP']
    proxyList = []
    for ip in df['IP']:
        proxyList.append('http://'+ip)
    return proxyList
proxyList = getIP()
# def getProxies():
#     proxyIp = random.choice(proxyList)
#     proxies = {'http':proxyIp}
#     return proxies
successIp = []

def test(n):
    time.sleep(3)
    url = 'http://www.gitdata.tw/'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0', }
    proxyIp = proxyList[n]
    proxies = {'http':proxyIp}
    try:
        print proxies
        req = requests.get(url,headers=header,proxies = proxies)
        print proxyIp +"可用"
        f = open(r'.\src\successIp.txt', 'a+')
        f.write(proxyIp + '\n')
        f.close()
    except requests.exceptions.ProxyError as e:
        print '代理失效'
    except requests.exceptions.ConnectionError as e:
        print '超时'


threads= []
for i in range(len(proxyList)):
    thread = threading.Thread(target=test,args=[i])
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()
