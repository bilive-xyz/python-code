#!usr/bin/env python
# -*- coding:utf-8 -*-

import html_downloader
import html_outputer
import html_parser
import url_manager

class SpiderMain(object):
    def __init__(self):
        self.urls=url_manager.UrlManager()      #url管理器
        self.downloader=html_downloader.HtmlDownloader()        #下载器
        self.parser=html_parser.HtmlParser()        #解析器
        self.outputer=html_outputer.HtmlOutputer()        #输出器

    def craw(self,root_url):
        count=1
        self.urls.add_new_url(root_url)     #将url加入url管理器
        while self.urls.has_new_url():      #是否有新的url
            try:
                new_url=self.urls.get_new_url()
                print ('craw %d: %s' % (count,new_url))
                html_cont=self.downloader.download(new_url)     #下载
                new_urls,new_data=self.parser.parse(new_url,html_cont)
                self.urls.add_new_urls(new_urls)    #把解析出的url加到url管理器
                self.outputer.collect_data(new_data)
                count+=1
            except:
                print ('craw failed')
        self.outputer.output_html()

if __name__ == "__main__":
    root_url='http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
    obj_spider=SpiderMain()
    obj_spider.craw(root_url)