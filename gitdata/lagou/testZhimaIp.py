# -*- coding:utf-8 -*-
"""
@Time       : 10:10
@Author     :邹文涛
@File       :testZhimaIp.py
"""

import time
import requests

class testZhimaIp:
    def __init__(self):
        text = open(r'.\src\IP\Ip.txt').read()
        self.proxyIpList = text.split('\n')


    def IP(self,num):
        proxyIp = self.proxyIpList[num]
        proxyies = {'http':proxyIp}
        return proxyies
    def urlTest(self):
        url = 'http://www.whatismyip.com.tw/'
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0'}
        for num in range(int(len(self.proxyIpList))):
            try:
                proxies = self.IP(num)
                req = requests.get(url,headers=header,proxies=proxies)
                print num
            except requests.exceptions.ProxyError as e:
                print '代理失效'
            except requests.exceptions.ConnectionError as e:
                print '超时'

if __name__ == '__main__':
    a = testZhimaIp()
    a.urlTest()