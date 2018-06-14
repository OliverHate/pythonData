# -*- coding:utf-8 -*-
"""
@Time       :2018/6/13 9:47
@Author     :邹文涛
@File       :notePc.py
@Software: PyCharm
"""

import urllib2
import re
import pandas as pd


class NotePc():

    def __init__(self):
        self.url_template = 'http://www.manmanbuy.com/cpl_86_qz_0_0_0_0_0_0_0_0_0_0_0_{}.aspx'
        reg = """<div class="sales">全网有<span>(.*?)</span>.*?<div class="btns"><a href=.*?addCompare\('(.*?)','(.*?)','.*?','(.*?)'\);" .*?</div>"""
        self.reg = re.compile(reg, re.S)

    # 获取源代码
    def getSourceCode(self, url):
        req = urllib2.Request(url=url)
        res = urllib2.urlopen(req)
        source_code = res.read().decode("gbk").encode("utf8")
        return source_code

    # 获取笔记本列表信息，并写入CSV文件
    def getNotePcList(self, source_code):
        note_pc_list = self.reg.findall(source_code)
        df = pd.DataFrame(data=note_pc_list)
        df.to_csv(r'..\data\NotePc.csv', mode='a+', index=None, header=None, sep=';')
        print df

    # 程序入口
    def main(self):
        for i in xrange(87):
            i += 1
            url = self.url_template.format(i)
            source_code = self.getSourceCode(url=url)
            self.getNotePcList(source_code)


if __name__ == '__main__':
    notePc = NotePc()
    notePc.main()
