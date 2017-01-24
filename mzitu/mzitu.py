#!usr/bin/env python
# -*- coding:utf-8 -*-

import os,re
from lxml import etree
import requests


class mzitu():
    def get_all_urls(self,url):
        html=self.request(url)      #传入request获取对象
        selector = etree.HTML(html.text)
        all_urls=selector.xpath('//ul[@class="archives"]/li/p[@class="url"]/a')
        for links in all_urls:
            url=links.attrib['href']        #获得url
            title=links.text                 #标题
            print u'开始下载：%s' % title
            name = re.sub('[\/:*?"<>|]', '-', title)        #剔除非法字符
            self.mkdir(name)        #创建文件夹
            path=os.path.join(r'F:/pictures', name)
            os.chdir(path)      #讲路径加入当前工作环境
            self.get_page_url(url)

    def get_page_url(self,url):
        html=requests.get(url)
        selector = etree.HTML(html.text)
        pages=selector.xpath('//div[@class="pagenavi"]/a/span')[-2].text
        for page in range(1,int(pages)+1):
            page_url=url + '/'+str(page)
            self.get_img_url(page_url)

    def get_img_url(self,page_url):
        img_html=self.request(page_url)
        img_url=re.findall(r'<img src="(.*?)"',img_html.text,re.S)  #正则提取图片url
        self.down_img(img_url)

    def down_img(self,img_url):
        name=img_url[0][-9:-4]      #img_url是一个list列表，先提取出来再切片
        print img_url
        img=self.request(img_url[0])
        with open(name +'.jpg','ab') as f:
            f.write(img.content)
            f.close()

    def mkdir(self,path):
        path = path.strip()     #移除字符串头尾空格
        isExists = os.path.exists(os.path.join(r'F:/pictures', path))
        if not isExists:
            os.makedirs(os.path.join(r'F:/pictures', path))

    def request(self, url):
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        content = requests.get(url, headers=headers)
        return content

Mzitu  = mzitu()  #实例化
Mzitu.get_all_urls('http://www.mzitu.com/all')