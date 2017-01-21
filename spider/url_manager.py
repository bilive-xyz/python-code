#!usr/bin/env python
# -*- coding:utf-8 -*-

class UrlManager(object):
    def __init__(self):
        self.new_urls=set()     #set()防止重复url
        self.old_urls=set()
    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, new_url):
        if new_url is None or len(new_url)==0:
            return
        for url in new_url:
            self.add_new_url(url)

    def has_new_url(self):
        return len(self.new_urls) !=0

    def get_new_url(self):
        new_url=self.new_urls.pop()     #取出url
        self.old_urls.add(new_url)      #加入到已爬取的url
        return new_url

