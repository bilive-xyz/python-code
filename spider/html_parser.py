#!usr/bin/env python
# -*- coding:utf-8 -*-
import re
import urlparse
from bs4 import BeautifulSoup

class HtmlParser(object):
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return None
        soup =BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')      #用bs4基础解析器
        new_urls=self._get_new_urls(page_url,soup)
        new_data=self._get_new_data(page_url,soup)
        return new_urls,new_data

    def _get_new_urls(self, page_url, soup):
        new_urls=set()
        #获得所有url链接
        links=soup.find_all('a',href=re.compile("/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/\.*"))
        for link in links:
            new_url=link['href']
            #urljoin拼接URL，它以base作为其基地址，然后与url中的相对地址相结合组成一个绝对URL地址
            new_full_url=urlparse.urljoin(page_url,new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data={}
        title_node=soup.find('h4')
        res_data['title']=title_node.get_text()
        summary_node=soup.find('div',class_="x-wiki-content")
        res_data['summary'] = summary_node.get_text()
        return res_data