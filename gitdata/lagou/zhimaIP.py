# -*- coding:utf-8 -*-
"""
@Time       : 10:01
@Author     :邹文涛
@File       :zhimaIP.py
"""
import requests
import re
import time
class getZhimaIP:
    def __init__(self):
        self.ipApi = 'http://webapi.http.zhimacangku.com/getip?num=20&type=2&pro=&city=0&yys=0&port=1&pack=12916&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
        self.header = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept - Encoding':'gzip, deflate',
        'Accept - Language':'zh - CN, zh;q = 0.8, zh - TW;q = 0.7, zh - HK;q = 0.5, en - US;q = 0.3, en;q = 0.2',
        'Cache - Control':'max - age = 0',
        'Connection':'keep - alive',
        'Cookie':'auto_login = 2d7039dad1ce3a037055b5475b306d4a;PHPSESSID = 92vphd43iv10s53m9u12kh6kk4',
        'Host':'web.http.cnapi.cc',
        'Upgrade - Insecure - Requests':'1',
        'User-Agent':  'Mozilla / 5.0(Windows NT 10.0; WOW64; rv:58.0) Gecko / 20100101 Firefox / 58.0'
           }
    def getIp(self):
        htmlJson =requests.get(url=self.ipApi,headers = self.header)
        getIpSuccess = htmlJson.json()['success']
        if getIpSuccess:
            with open(r'src\ip\Ip.txt', 'a+') as f:
                for ipPort in htmlJson.json()['data']:
                    ip = ':'.join([ipPort.get('ip').encode('utf-8'),str(ipPort.get('port'))])
                    # f.write( 'http://'+ip+'\n')
                    f.write(ip + '\n')
            f.close()
            print '写入完毕'
        else:
            print htmlJson.json()['msg']
            reg = r'([0-9]{1,3})'
            reg = re.compile(reg)
            ip = re.findall(reg,htmlJson.json()['msg'])
            ip = '.'.join(ip)
            self.setWhitIp(ip)

    def setWhitIp(self,ip):
        whiteIpApi = 'http://web.http.cnapi.cc/index/index/save_white?neek=36134&appkey=e19304d675585d2eb98121bb96f7fc61&white={}'.format(ip)
        push = {'appkey':'e19304d675585d2eb98121bb96f7fc61','neek':'36134','white'	:ip}
        html = requests.get(whiteIpApi,data=push,headers = self.header)
        self.getIp()
        print ip.encode('utf-8')+'已添加完毕'


    # def getAppkey(self):
    #     header = {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #         'Accept - Encoding': 'gzip, deflate',
    #         'Accept - Language': 'zh - CN, zh;q = 0.8, zh - TW;q = 0.7, zh - HK;q = 0.5, en - US;q = 0.3, en;q = 0.2',
    #         'Cache - Control': 'max - age = 0',
    #         'Connection': 'keep - alive',
    #         'Referer':'http://h.zhimaruanjian.com / wirte_list/',
    #         'Cookie': 'auto_login = 2d7039dad1ce3a037055b5475b306d4a;PHPSESSID = 92vphd43iv10s53m9u12kh6kk4',
    #         'Upgrade - Insecure - Requests':'1',
    #         'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; WOW64; rv:58.0) Gecko / 20100101 Firefox / 58.0'
    #     }
    #     appKeyApi = 'http://web.http.cnapi.cc/index/index/get_white_link'
    #     html = requests.get(appKeyApi,headers = header)
    #     print html.text
    #
    # def login(self):
    #     loginApi = 'http://web.http.cnapi.cc/index/users/login_do?jsonpcallback=jQuery112406299922093280768_1517894145041&phone=t794762&password=794762&remember=false&_=1517894145044'
    #     header = {
    #         'Accept': '* / *',
    #         'Accept - Encoding': 'gzip, deflate',
    #         'Accept - Language': 'zh - CN, zh;q = 0.8, zh - TW;q = 0.7, zh - HK;q = 0.5, en - US;q = 0.3, en;q = 0.2',
    #         'Connection': 'keep - alive',
    #         'Cookie': 'auto_login = 2d7039dad1ce3a037055b5475b306d4a;PHPSESSID = 92vphd43iv10s53m9u12kh6kk4',
    #         'Host': 'web.http.cnapi.cc',
    #         'Referer': 'http: // h.zhimaruanjian.com /',
    #         'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; WOW64; rv:58.0) Gecko / 20100101 Firefox / 58.0'
    #     }
    #     push = {
    #      '_':'1517894145044',
    #     'jsonpcallback':'jQuery112406299922093280768_1517894145041',
    #     'password':'794762',
    #     'phone':'t794762',
    #     'remember':'false'
    #     }
    #     html = requests.get(loginApi,data = push,headers = header)
    #     print html.text


if __name__ == '__main__':
    ip = getZhimaIP()
    for i in range(6):
        time.sleep(5)
        ip.getIp()
